#from evdev import InputDevice
import evdev
from select import select

#DEVICE = ('/dev/input/event3', '/dev/input/event2','/dev/input/event6')
DEVICE = ('/dev/input/event2')
print(type(DEVICE))

if isinstance(DEVICE, tuple): 
    devices = map(evdev.InputDevice, DEVICE)
    devices = {dev.fd: dev for dev in devices}

    for dev in devices.values(): print(dev)

    while True:
        r, w, x = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if event.type == evdev.ecodes.EV_KEY or event.type == evdev.ecodes.EV_REL:
                    print(event)
else:
    device = evdev.InputDevice(DEVICE)
    print(device)
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY or event.type == evdev.ecodes.EV_REL:
            print(event)
