import evdev
import asyncio

async def handle_events(device):
    async for event in device.async_read_loop():
            print("==============================")
            print("name:",device.name)
            print("vendor_id:",device.info.vendor)
            print("product_id:",device.info.product)
            print(event)

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
