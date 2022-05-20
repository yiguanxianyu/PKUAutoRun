# -*- coding:utf-8 -*
from pathlib import Path

from pymobiledevice3.services.mobile_image_mounter import MobileImageMounterService
from wget import download


# from zipfile import ZipFile


def download_image(ios_version):
    base_dir = './Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/'
    base_url = 'https://raw.fastgit.org/pdso/DeveloperDiskImage/master/{}/DeveloperDiskImage.dmg'

    img_dir = base_dir + ios_version + '/.DeveloperDiskImage.dmg'
    sig_dir = base_dir + ios_version + '/.DeveloperDiskImage.dmg.signature'
    img_url = base_url.format(ios_version)
    sig_url = img_url + '.signature'

    Path(base_dir).mkdir(parents=True, exist_ok=True)

    print('开始下载模拟所需的开发者镜像文件')
    if not (Path(img_dir).exists() and Path(sig_dir).exists()):
        print('···正在下载镜像文件，此过程可能较费时，请耐心等待')
        download(img_url, base_dir)
        download(sig_url, base_dir)
    else:
        print('···镜像文件已存在')
    print('镜像下载完成')

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
        return

    download_image(version)

    image = f'./Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/{version}/DeveloperDiskImage.dmg'
    signature = image + '.signature'

    image = Path(image)
    image = image.read_bytes()

    signature = Path(signature)
    signature = signature.read_bytes()

    image_mounter.upload_image(image_type, image, signature)
    image_mounter.mount(image_type, signature)

    print('镜像挂载成功')
