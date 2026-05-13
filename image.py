# -*- coding:utf-8 -*
from pathlib import Path

from pymobiledevice3.services.mobile_image_mounter import MobileImageMounterService

from requests import get


def download_image(ios_version):
    base_dir = f'./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{ios_version}'
    base_url = f'https://ghproxy.net/https://raw.githubusercontent.com/pdso/DeveloperDiskImage/master/{ios_version[0:2]}/{ios_version}/DeveloperDiskImage.dmg'

    img_path = Path(base_dir) / 'DeveloperDiskImage.dmg'
    sig_path = img_path.with_suffix('.dmg.signature')

    Path(base_dir).mkdir(parents=True, exist_ok=True)

    print('开始下载模拟所需的开发者镜像文件')

    if img_path.exists():
        print('···镜像文件已存在')
    else:
        print('···正在下载镜像文件，此过程可能较费时，请耐心等待')
        resp = get(base_url, allow_redirects=True, timeout=300)
        resp.raise_for_status()
        img_path.write_bytes(resp.content)
        print('镜像下载完成')

    if sig_path.exists():
        print('···镜像签名文件已存在')
    else:
        print('···正在下载镜像签名文件，此过程可能较费时，请耐心等待')
        resp = get(f'{base_url}.signature', allow_redirects=True, timeout=120)
        resp.raise_for_status()
        sig_path.write_bytes(resp.content)
        print('镜像签名下载完成')


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

    img_path = Path(f'./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{version}/DeveloperDiskImage.dmg')
    sig_path = img_path.with_suffix('.dmg.signature')

    image = img_path.read_bytes()
    signature = sig_path.read_bytes()

    image_mounter.upload_image(image_type, image, signature)

    try:
        image_mounter.mount(image_type, signature)
        print('镜像挂载成功')
        return 1

    except Exception as mount_err:
        # 原逻辑把「任意挂载失败」都当成 iOS 16+ 去调 AmfiService；iOS 15 无该服务会报 InvalidService。
        product_version = lockdown.all_values.get('ProductVersion', '0')
        try:
            ios_major = int(str(product_version).split('.')[0])
        except (TypeError, ValueError):
            ios_major = 0

        if ios_major < 16:
            print('镜像挂载失败（当前系统低于 iOS 16，不会尝试开启开发者模式）。')
            print('常见原因：开发者镜像与系统不完全匹配、下载不完整、设备未解锁或屏幕未亮。')
            print(f'原始错误: {mount_err}')
            return 0

        print(
            'iOS 16 以上系统需要先开启开发者模式才能运行，此部分请参考项目README。正在尝试为你开启开发者模式……'
        )
        from pymobiledevice3.exceptions import DeviceHasPasscodeSetError
        from pymobiledevice3.services.amfi import AmfiService
        from pymobiledevice3.services.diagnostics import DiagnosticsService

        try:
            AmfiService(lockdown).enable_developer_mode()
            print('已开启开发者模式，正在重启设备。请在设备重启后确认打开开发者模式，并重新运行本程序。')
            DiagnosticsService(lockdown).restart()
        except DeviceHasPasscodeSetError:
            print('开发者模式开启失败，需要先关闭设备密码以打开开发者模式。')
        except Exception as amfi_err:
            print(f'尝试开启开发者模式失败: {amfi_err}')

        return 0
