import evdev
from select import select
import subprocess
import time
import datetime
from volumio_com import *
import os
import asyncio
path = 'voco_usr_init.py'
is_file = os.path.isfile(path)
if is_file:
    print(is_file)
    from voco_usr_init import *
    print("import voco_usr_init")
else:
    print(is_file)
    from voco_init import *
    print("import voco_init")

print(f"#----------voco start---{datetime.datetime.now()}---------")

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

def inputCTL(event,device):
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
        if len(x) <= 7:
            intVID = ""
            intPID = ""
        else:
            intVID = x[7]
            intPID = x[8]

        if intX == "":
           intX = rel_x
        if intY == "":
           intY = rel_y
        if intH == "":
           intH = rel_h

        if intVID == "":
            intVID = device.info.vendor
        if intPID == "":
            intPID = device.info.product

        if event.type == intType and event.code == intCode and rel_x == intX and rel_y == intY and rel_h == intH and event.value == intValue and intVID == device.info.vendor and intPID == device.info.product:
            print(x)
            print(f"type = {intType}")
            print(f"code = {intCode}")
            print(f"vender = {device.info.vendor}")
            print(f"product = {device.info.product}")
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

async def handle_events(device):
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_KEY or event.type == evdev.ecodes.EV_REL:
            print("==============================")
            print(device.name)
            print(event)
            getREL(event)
            print(f"rel_x={rel_x} rel_y={rel_y} rel_h={rel_h}")
            inputCTL(event,device) 

async def watch_devices():
    devices = set(evdev.list_devices())
    for device_path in devices:
        device = evdev.InputDevice(device_path)
        asyncio.create_task(handle_events(device))
        print("Device added:", device_path,device.name)

    while True:
        new_devices = set(evdev.list_devices())
        added_devices = new_devices - devices
        removed_devices = devices - new_devices

        for device_path in added_devices:
            device = evdev.InputDevice(device_path)
            asyncio.create_task(handle_events(device))
            print("Device added:", device_path,device.name)

        for device_path in removed_devices:
            # 削除されたデバイスに対する処理を追加する
            print("Device removed:", device_path)

        devices = new_devices

        # イベントの取得を待つ
        await asyncio.sleep(1)

async def main():
    await watch_devices()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
