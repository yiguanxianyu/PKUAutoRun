import image
from preprocessing import PreProcesser
from pymobiledevice3.usbmux import list_devices
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.simulate_location import DtSimulateLocation


def play_gpx(lockdown, filename):
    print("开始模拟跑步")
    location_simulator = DtSimulateLocation(lockdown=lockdown)
    location_simulator.play_gpx_file(filename)
    location_simulator.clear()
    print("跑步完成，请在手机中结束跑步")


def main(gpx_path):
    device_list = list_devices()
    if not device_list:
        print("未查找到设备，请确认：")
        print("  1. 是否已下载并安装 iTunes")
        print("  2. 是否已将设备连接到电脑、解锁设备并勾选信任选项")
        input("按下回车退出")
        return

    device = device_list[0]
    device_id = device.serial

    device_LockdownClient = LockdownClient(device_id)
    device_info = device_LockdownClient.all_values

    ios_version = device_info["ProductVersion"]
    device_name = device_info["DeviceName"]

    print(f"已连接到您的设备：{device_name}, iOS/iPadOS 版本为{ios_version}。")
    print("请保证在镜像挂载完成之前手机已解锁且屏幕亮起。")

    ios_version = ios_version[0:4]
    ios_version_replace = {"14.8": "14.7", "15.1": "15.0"}
    if ios_version in ios_version_replace.keys():
        ios_version = ios_version_replace[ios_version]

    image.mount_image(device_LockdownClient, ios_version)
    pps = PreProcesser(gpx_path)
    pps.show_info()
    play_gpx(device_LockdownClient, "./preprocessed/tempgpx.gpx")
    image.unmount_image(device_LockdownClient)
    input("跑步完成，按下回车键退出")


if __name__ == "__main__":
    print(r"""
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|

""")

    main(r"./samples/54_5.1km.gpx")
