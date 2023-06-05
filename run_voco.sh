#!/bin/bash

#sleep 120

/usr/bin/python3 -u /home/volumio/voco/voco.py >> /home/volumio/voco/log/voco_log_$(date +"%y%m%d_%H%M%S").txt 2>&1 &

