# -*- coding:utf-8 -*
from pathlib import Path

from pymobiledevice3.services.mobile_image_mounter import MobileImageMounterService

from requests import get


def download_image(ios_version):
    base_dir = f'./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{ios_version}'
    base_url = f'https://fastly.jsdelivr.net/gh/pdso/DeveloperDiskImage@master/{ios_version}/DeveloperDiskImage.dmg'

    img_dir = base_dir + '/DeveloperDiskImage.dmg'
    img_url = base_url
    sig_dir = img_dir + '.signature'
    sig_url = img_url + '.signature'

    Path(base_dir).mkdir(parents=True, exist_ok=True)

    print('开始下载模拟所需的开发者镜像文件')

    if Path(img_dir).exists():
        print('···镜像文件已存在')
    else:
        print('···正在下载镜像文件，此过程可能较费时，请耐心等待')
        img = get(img_url, allow_redirects=True)
        open(img_dir, 'wb').write(img.content)
        print('镜像下载完成')

    if Path(sig_dir).exists():
        print('···镜像签名文件已存在')
    else:
        print('···正在下载镜像签名文件，此过程可能较费时，请耐心等待')
        sig = get(sig_url, allow_redirects=True)
        open(sig_dir, 'wb').write(sig.content)
        print('镜像签名下载完成')

    # from zipfile import ZipFile
    # with ZipFile(img_dir) as zf:
    #     zf.extractall(base_dir)
    #     print('镜像解压缩完成')


def unmount_image(lockdown):
    image_type = 'Developer'
    mount_path = '/Developer'
    image_mounter = MobileImageMounterService(lockdown=lockdown)
    image_mounter.umount(image_type, mount_path, b'')
    print('成功卸载镜像')


def mount_image(lockdown, version):
    image_type = 'Developer'

    image_mounter = MobileImageMounterService(lockdown=lockdown)
    if image_mounter.is_image_mounted(image_type):
        print('镜像已经被挂载过了')
        return 1

    download_image(version)

    image = f'./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{version}/DeveloperDiskImage.dmg'
    signature = image + '.signature'

    image = Path(image).read_bytes()
    signature = Path(signature).read_bytes()

    image_mounter.upload_image(image_type, image, signature)

    try:
        image_mounter.mount(image_type, signature)
        print('镜像挂载成功')
        return 1

    except Exception:
        print(f'iOS 16 以上系统需要先开启开发者模式才能运行，此部分请参考项目README。正在尝试为你开启开发者模式……')
        from pymobiledevice3.exceptions import DeviceHasPasscodeSetError
        from pymobiledevice3.services.amfi import AmfiService
        from pymobiledevice3.services.diagnostics import DiagnosticsService

        try:
            AmfiService(lockdown).enable_developer_mode()
            print('已开启开发者模式，正在重启设备。请在设备重启后确认打开开发者模式，并重新运行本程序。')
            DiagnosticsService(lockdown).restart()
        except DeviceHasPasscodeSetError:
            print('开发者模式开启失败，需要先关闭设备密码以打开开发者模式。')

        return 0
