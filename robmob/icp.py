import numpy as np


def best_fit_transform(A, B):
    """
    Calculates the least-squares best-fit transform between corresponding 3D points A->B
    Input:
      A: Nx3 numpy array of corresponding 3D points
      B: Nx3 numpy array of corresponding 3D points
    Returns:
      T: 4x4 homogeneous transformation matrix
      R: 3x3 rotation matrix
      t: 3x1 column vector
    """

    assert len(A) == len(B)

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R, centroid_A.T)

    # homogeneous transformation
    T = np.identity(4)
    T[0:3, 0:3] = R
    T[0:3, 3] = t

    return T, R, t


def nearest_neighbor(src, dst):
    """
    Find the nearest (Euclidean) neighbor in dst for each point in src
    Input:
        src: Nx3 array of points
        dst: Nx3 array of points
    Output:
        distances: Euclidean distances (errors) of the nearest neighbor
        indecies: dst indecies of the nearest neighbor
    """

    indecies = np.zeros(src.shape[0], dtype=int)
    distances = np.zeros(src.shape[0])
    for i, s in enumerate(src):
        distances_mat = np.linalg.norm(dst[:] - s, axis=1)
        indecies[i] = np.argmin(distances_mat)
        distances[i] = distances_mat[indecies[i]]

    return distances, indecies


def homogeneous_copy_of_pcl(pcl):
    """
    Input:
        pcl: Nx3 or Nx4 numpy array of 3D points.
    Output:
        A deep copy of the point cloud, in homogeneous coordinates.
        If the input matrix had 4 columns, it is returned as is.
    """
    if pcl.shape[1] == 4:
        return np.copy(pcl.T)
    elif pcl.shape[1] == 3:
        copy_of_pcl = np.copy(pcl)
        return np.concatenate((copy_of_pcl.T, np.ones((1, copy_of_pcl.shape[0]))), axis=0)


def icp(A, B, init_pose=None, max_iterations=50, tolerance=0.001):
    """
    The Iterative Closest Point method
    Input:
        A: Nx3 or Nx4 numpy array of source 3D points
        B: Nx3 or Nx4 numpy array of destination 3D point
        init_pose: 4x4 homogeneous transformation
        max_iterations: exit algorithm after max_iterations
        tolerance: convergence criteria
    Output:
        T: final homogeneous transformation
        distances: Euclidean distances (errors) of the nearest neighbor
    """

    # Convert the points to homogeneous coordinates.
    src = homogeneous_copy_of_pcl(A)
    dst = homogeneous_copy_of_pcl(B)

    # apply the initial pose estimation
    if init_pose is not None:
        src = np.dot(init_pose, src)

    prev_error = 0

    for i in range(max_iterations):
        # find the nearest neighbours between the current source and destination points
        distances, indices = nearest_neighbor(src[0:3, :].T, dst[0:3, :].T)

        # compute the transformation between the current source and nearest destination points
        T, _, _ = best_fit_transform(src[0:3, :].T, dst[0:3, indices].T)

        # update the current source
        src = np.dot(T, src)

        # check error
        mean_error = np.average(distances)
        print('Mean distance between associated points: {}'.format(mean_error))
        if abs(prev_error - mean_error) < tolerance:
            break
        prev_error = mean_error

    # calculcate final tranformation
    T, _, _ = best_fit_transform(A[:, 0:3], src[0:3, :].T)

    return T, distances
