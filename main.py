from pathlib import Path
from wget import download
from zipfile import ZipFile

from pymobiledevice3.usbmux import list_devices
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.simulate_location import DtSimulateLocation
from pymobiledevice3.services.mobile_image_mounter import MobileImageMounterService


def download_image(ios_version):
    base_dir = "./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/"
    base_url = "https://raw.fastgit.org/filsv/iPhoneOSDeviceSupport/master/"

    img_dir = base_dir + ios_version + ".zip"
    img_url = base_url + ios_version + ".zip"

    Path(base_dir).mkdir(parents=True, exist_ok=True)

    print("开始下载模拟所需的开发者镜像文件")
    if not Path(img_dir).exists():
        print("···正在下载镜像文件，此过程可能较费时，请耐心等待")
        download(img_url, base_dir)
        print()
    else:
        print("···镜像文件已存在")
    print("镜像下载完成")

    with ZipFile(img_dir) as zf:
        zf.extractall(base_dir)
        print("镜像解压缩完成")


def play_gpx(lockdown, filename):
    print("开始模拟跑步")
    location_simulator = DtSimulateLocation(lockdown=lockdown)
    location_simulator.play_gpx_file(filename)
    location_simulator.clear()
    print("跑步完成，请在手机中结束跑步")


def unmount_image(lockdown):
    image_type = "Developer"
    mount_path = "/Developer"
    image_mounter = MobileImageMounterService(lockdown=lockdown)
    image_mounter.umount(image_type, mount_path, b"")
    print("成功卸载镜像")


def mount_image(lockdown, version):
    image_type = "Developer"

    image_mounter = MobileImageMounterService(lockdown=lockdown)
    if image_mounter.is_image_mounted(image_type):
        print("镜像已经被挂载过了")
        return

    download_image(version)

    image = f"./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{version}/DeveloperDiskImage.dmg"
    signature = image + ".signature"

    image = Path(image)
    image = image.read_bytes()

    signature = Path(signature)
    signature = signature.read_bytes()

    image_mounter.upload_image(image_type, image, signature)
    image_mounter.mount(image_type, signature)

    print("镜像挂载成功")


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
    ios_version_replace = {"14.8": "14.7"}
    if ios_version in ios_version_replace.keys():
        ios_version = ios_version_replace[ios_version]

    mount_image(device_LockdownClient, ios_version)
    play_gpx(device_LockdownClient, gpx_path)
    unmount_image(device_LockdownClient)
    input("按下回车键退出")


if __name__ == "__main__":
    print(r"""
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|

""")

    main(r"./samples\54_36m15s_5.1km.gpx")
