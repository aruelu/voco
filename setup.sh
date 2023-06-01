#!/bin/bash

sudo apt update
sudo apt install -y python3-pip
sudo pip3 install evdev

sudo ln -s /home/volumio/voco/run_voco.sh /etc/init.d/run_voco.sh
sudo ln -s /etc/init.d/run_voco.sh /etc/rc1.d/S01run_voco.sh
sudo ln -s /etc/init.d/run_voco.sh /etc/rc2.d/S01run_voco.sh
sudo ln -s /etc/init.d/run_voco.sh /etc/rc3.d/S01run_voco.sh
sudo ln -s /etc/init.d/run_voco.sh /etc/rc4.d/S01run_voco.sh
sudo ln -s /etc/init.d/run_voco.sh /etc/rc5.d/S01run_voco.sh
