import asyncio

from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.services.simulate_location import DtSimulateLocation
from pymobiledevice3.usbmux import list_devices

import image
from preprocessing import PreProcessor


async def set_loc(location_simulator, lat, lon, sleep_time):
    await asyncio.sleep(sleep_time)
    location_simulator.set(lat, lon)


def auto_run(points, location_simulator):
    start_time = points[0].time
    loop = asyncio.get_event_loop()

    print('开始模拟跑步')
    loop.run_until_complete(
        asyncio.gather(*(
            set_loc(location_simulator,
                    p.latitude,
                    p.longitude,
                    (p.time - start_time).total_seconds())
            for p in points
        ))
    )


def main(gpx_path, run_speed):
    device_list = list_devices()
    if not device_list:
        print('未查找到设备，请确认：')
        print('  1. 是否已下载并安装 iTunes')
        print('  2. 是否已将设备连接到电脑、解锁设备并勾选信任选项')
        input('按下回车退出')
        return

    num_devices = len(device_list)
    if num_devices > 1:
        print('发现多台设备:')

        for i in range(num_devices):
            print(i, LockdownClient(device_list[i].serial).all_values['DeviceName'])

        index = int(input('请输入对应数字以选择设备: '))
        device = device_list[index]

    else:
        device = device_list[0]

    device_lockdown_client = LockdownClient(device.serial)
    location_simulator = DtSimulateLocation(device_lockdown_client)

    device_info = device_lockdown_client.all_values
    device_class = device_info['DeviceClass']
    ios_version = device_info['ProductVersion'][0:4]
    device_name = device_info['DeviceName']

    print(f'已连接到您的 {device_class}: {device_name}, iOS/iPadOS 版本为 {ios_version}。')
    print('请确保在镜像挂载完成之前手机已解锁且屏幕亮起。')

    ios_version_replace = {'14.8': '14.7', '15.1': '15.0'}
    if ios_version in ios_version_replace:
        ios_version = ios_version_replace[ios_version]

    image.mount_image(device_lockdown_client, ios_version)

    pps = PreProcessor(gpx_path, run_speed)
    pps.show_info()
    auto_run(pps.points, location_simulator)

    image.unmount_image(device_lockdown_client)

    print('跑步完成, 请在手机上结束跑步。建议您重启设备。\n'
          '- 输入 0 以清除定位但不重启设备；\n'
          '- 输入 1 以清除定位并且重启设备；\n'
          '- 如果什么也不做，可以直接退出程序。')

    arg = input()
    if arg == '0':
        location_simulator.clear()
    elif arg == '1':
        DiagnosticsService(device_lockdown_client).restart()


if __name__ == '__main__':
    print(r'''
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|

提示: 如果要使用多台设备同时打卡, 请多开本程序
''')

    path = input('请输入 GPX 文件路径或将文件拖入到这里：')
    speed = int(input('请输入你希望的平均配速(秒), 如五分配速输入300:'))

    # 如果在 Python 脚本中运行程序，可以直接在下面修改路径使用：
    # path = r'./samples/54_6.5km.gpx'
    # speed = 280
    main(path, speed)
