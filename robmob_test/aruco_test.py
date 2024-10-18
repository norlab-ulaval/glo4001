import time
import unittest

import cv2
import matplotlib.pyplot as plt

from robmob.robot import Robot
from robmob.rover.commands import ResetCommand, MovementPWMCommand
from robmob.rover.sensors import RobotEspSensor, SharpSensor, CameraRGBSensor, CameraDepthSensor, OakLiteCamera

class TestRobot(unittest.TestCase):
    def test_connect(self):
        capture = cv2.VideoCapture(0)
        ret, frame = capture.read()
        capture.release()
        plt.imshow(frame)
        plt.show()

        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict,
                                                           parameters=arucoParams)



