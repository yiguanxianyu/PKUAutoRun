import image
from preprocessing import PreProcessor
from pymobiledevice3.usbmux import list_devices
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
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

    device_lockdown_client = LockdownClient(device_id)
    device_info = device_lockdown_client.all_values

    ios_version = device_info["ProductVersion"]
    device_name = device_info["DeviceName"]

    print(f"已连接到您的设备：{device_name}, iOS/iPadOS 版本为{ios_version}。")
    print("请保证在镜像挂载完成之前手机已解锁且屏幕亮起。")

    ios_version = ios_version[0:4]
    ios_version_replace = {"14.8": "14.7", "15.1": "15.0"}
    if ios_version in ios_version_replace.keys():
        ios_version = ios_version_replace[ios_version]

    image.mount_image(device_lockdown_client, ios_version)
    pps = PreProcessor(gpx_path)
    pps.show_info()
    play_gpx(device_lockdown_client, "./preprocessed/temp-gpx.gpx")
    image.unmount_image(device_lockdown_client)

    arg = input("跑步完成，请重启手机。输入1将自动重启")
    if arg == 1:
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
    # path = input("请输入 GPX 文件路径或将文件拖入到这里并按下回车：")
    path = r"./samples/54_6.5km.gpx"
    main(path)
