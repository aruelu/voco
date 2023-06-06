import evdev
from select import select
import subprocess
import time
import datetime
from volumio_com import *
import os
path = 'voco_usr_init.py'
is_file = os.path.isfile(path)
if is_file:
    print(is_file)
    from voco_usr_init import *
else:
    print(is_file)
    from voco_init import *

print(type(DEVICE))
rel_x = 0
rel_y = 0
rel_h = 0
sd_cnt = 0
s_time = 0
e_time = 0

def getREL(self):
    global rel_x
    global rel_y
    global rel_h
    if self.type == evdev.ecodes.EV_REL:
        if self.code == evdev.ecodes.REL_X:
            rel_x = self.value
        elif self.code == evdev.ecodes.REL_Y:
            rel_y = self.value
        elif self.code == evdev.ecodes.REL_WHEEL:
            rel_h = self.value

def inputCTL():
    global sd_cnt
    global s_time
    global e_time
    for x in CTL:
        strCmd = x[0]
        intType = x[1]
        intCode = x[2]
        intX = x[3]
        intY = x[4]
        intH = x[5]
        intValue = x[6]
        if intX == "":
           intX = rel_x
        if intY == "":
           intY = rel_y
        if intH == "":
           intH = rel_h
        if event.type == intType and event.code == intCode and rel_x == intX and rel_y == intY and rel_h == intH and event.value == intValue :
            print(strCmd)
            if strCmd == "prev":
                prev()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "volup":
                volup()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "play":
                play()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "voldw":
                voldw()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "next":
                next()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "voltog":
                voltog()
                sd_cnt = 0
                print(f"sd_cnt = {sd_cnt}")
            elif strCmd == "shutdown":
                if sd_cnt == 4:
                    e_time =  time.perf_counter()
                    if e_time - s_time <= 5:
                        print(f"sd_cnt = {sd_cnt}")
                        print(f"s_time = {s_time}")
                        print(f"e_time = {e_time}")
                        print(f"e_time - s_time = {e_time - s_time}")
                        shutdown()
                    else:
                        print(f"sd_cnt = {sd_cnt}")
                        print(f"s_time = {s_time}")
                        print(f"e_time = {e_time}")
                        print(f"e_time - s_time = {e_time - s_time}")
                        print("sd_reset")
                        sd_cnt = 0
                        s_time = 0
                        e_time = 0
                elif sd_cnt == 0:
                    s_time = time.perf_counter()
                    e_time = 0
                    print(f"sd_cnt = {sd_cnt}")
                    print(f"s_time = {s_time}")
                    print(f"e_time = {e_time}")
                    sd_cnt += 1
                else:
                    print(f"sd_cnt = {sd_cnt}")
                    print(f"s_time = {s_time}")
                    print(f"e_time = {e_time}")
                    sd_cnt += 1
            break #forを抜ける


print(f"#----------voco start---{datetime.datetime.now()}---------")
from select import select
DEVICE = []

import glob

for name in glob.glob('/dev/input/event*'):
    print(name)
    DEVICE.append(name)

devices = map(evdev.InputDevice, DEVICE)
devices = {dev.fd: dev for dev in devices}

for dev in devices.values(): print(dev)

while True:
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            #if event.type == evdev.ecodes.EV_KEY or event.type == evdev.ecodes.EV_REL:
            print(event)
            if event.type == evdev.ecodes.EV_KEY or event.type == evdev.ecodes.EV_REL:
                print(event)
                getREL(event)
                print(f"rel_x={rel_x} rel_y={rel_y} rel_h={rel_h}")
                inputCTL() 
