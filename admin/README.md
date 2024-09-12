# Procedures to setup the robots

## Make the Orin image
Follow the instructions from: [Orin Setup](OrinSetup.md)

## Make the Jetson image
[Flashing](https://docs.nvidia.com/jetson/archives/r36.3/DeveloperGuide/SD/FlashingSupport.html?highlight=flashing#flashing-to-an-sd-card)

https://docs.nvidia.com/sdk-manager/docker-containers/index.html

https://unix.stackexchange.com/questions/132797/how-to-dd-a-remote-disk-using-ssh-on-local-machine-and-save-to-a-local-disk

```python
docker build -t jetson .
docker run --rm --privileged -v /dev:/dev -v /media/robmob/SDCARD:/media/robmob/SDCARD jetson
# share x11
docker run -it --rm --privileged -v /dev:/dev -v .:/app -e DISPLAY=$DISPLAY --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v /tmp/.X11-unix:/tmp/.X11-unix jetson bash


dpkg -i 
```

```shell
wget https://developer.nvidia.com/downloads/embedded/l4t/r36_release_v3.0/release/jetson_linux_r36.3.0_aarch64.tbz2
tar -xvf jetson_linux_r36.3.0_aarch64.tbz2


```

```shell
# ssh to orin
ssh user@remote "dd if=/dev/nvme0n1 | gzip -1 -" | dd of=image.gz
ssh user@remote "dd if=/dev/nvme0n1 | dd of=image.gz

sudo dd if=/dev/sda of=jetson_img.iso bs=1M oflag=direct status=progress
sudo dd if=image of=/dev/sda bs=1M oflag=direct status=progress
```

## Run commands on all robots

