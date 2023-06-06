import evdev
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
