# Procedures to setup the robots

## Make the Orin image
Follow the instructions from: [Orin Setup](OrinSetup.md)

## Flashing the Jetson image

```shell
# On the correctly configured Jetson
sudo dd if=/dev/sda of=jetson_img.iso bs=1M oflag=direct status=progress
tar -czvf jetson_img.iso.tar.gz jetson_img.iso

# On the computer
# Download the image
# Extract the image
tar -xzvf jetson_img.iso.tar.gz
# Plug the nvme drive and check the device
fdisk -l
pv -s 120G < jetson_img.iso > /dev/sda
```

## Final setup

```shell
# Change the password to `robmob`
sudo passwd norlab
# Get the code
git clone https://github.com/norlab-ulaval/glo4001
# Setup
~/glo4001/scripts/setup.sh
# Make a Wi-Fi hotspot with the name `team<robot-number>-wifi`
```