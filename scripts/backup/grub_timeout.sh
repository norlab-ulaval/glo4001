#!/bin/bash
cp /etc/default/grub /etc/default/grub.bak
sed 's/GRUB_HIDDEN_TIMEOUT=[0-9]\+/GRUB_HIDDEN_TIMEOUT=1/' /etc/default/grub.bak | sed 's/GRUB_TIMEOUT=[0-9]\+$/GRUB_TIMEOUT=0/' | tee /etc/default/grub
update-grub
