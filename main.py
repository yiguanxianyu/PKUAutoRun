import image
import asyncio
from preprocessing import PreProcessor
from pymobiledevice3.usbmux import list_devices
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.services.simulate_location import DtSimulateLocation


async def set_loc(location_simulator, lat, lon, sleep_time):
    await asyncio.sleep(sleep_time)
    location_simulator.set(lat, lon)


def auto_run(lockdown, points):
    location_simulator = DtSimulateLocation(lockdown=lockdown)

    start_time = points[0].time

    tasks = asyncio.gather(*(
        set_loc(location_simulator, p.latitude, p.longitude, (p.time - start_time).total_seconds())
        for p in points
    ))

    print("开始模拟跑步")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    location_simulator.clear()


def main(gpx_path, run_speed):
    device_list = list_devices()
    if not device_list:
        print("未查找到设备，请确认：")
        print("  1. 是否已下载并安装 iTunes")
        print("  2. 是否已将设备连接到电脑、解锁设备并勾选信任选项")
        input("按下回车退出")
        return

    device = device_list[0]
    device_id = device.serial

    device_lockdown_client = LockdownClient(device_id)
    device_info = device_lockdown_client.all_values

    ios_version = device_info["ProductVersion"][0:4]
    device_name = device_info["DeviceName"]

    print(f"已连接到您的设备：{device_name}, iOS/iPadOS 版本为{ios_version}。")
    print("请保证在镜像挂载完成之前手机已解锁且屏幕亮起。")

    ios_version_replace = {"14.8": "14.7", "15.1": "15.0"}
    if ios_version in ios_version_replace.keys():
        ios_version = ios_version_replace[ios_version]

    image.mount_image(device_lockdown_client, ios_version)

    pps = PreProcessor(gpx_path, run_speed)
    pps.show_info()
    auto_run(device_lockdown_client, pps.points)

    image.unmount_image(device_lockdown_client)

    arg = input("跑步完成，请在手机上结束跑步，然后重启设备。输入1将自动重启")
    if arg == "1":
        DiagnosticsService(device_lockdown_client).restart()


if __name__ == "__main__":
    print(r"""
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|

""")

    path = input("请输入 GPX 文件路径或将文件拖入到这里并按下回车：")
    speed = int(input("请输入你希望的配速，以秒为单位，如五分配速输入300.若不输入，默认为五分配速"))
    # 如果在 Python 脚本中运行程序，可以直接在下面修改路径使用：
    # path = r"./samples/54_6.5km.gpx"
    # speed = 260
    main(path, speed)
