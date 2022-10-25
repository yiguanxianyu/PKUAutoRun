# -*- coding:utf-8 -*
import asyncio
from datetime import datetime, timedelta

from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.services.simulate_location import DtSimulateLocation
from pymobiledevice3.usbmux import list_devices

import image
from gen_record import gen_record


async def auto_run(points, location_simulator):
    async def set_loc(lat, lon, t):
        await asyncio.sleep(t)
        location_simulator.set(lat, lon)

    await asyncio.gather(*(set_loc(*p) for p in points))


def main(distance, speed):
    device_list = list_devices()
    if not device_list:
        print('未查找到设备，请确认：')
        print('  1. 是否已下载并安装 iTunes')
        print('  2. 是否已将设备连接到电脑、解锁设备并勾选信任选项')
        input('按下回车退出')
        return

    num_devices = len(device_list)
    index = 0
    
    if num_devices > 1:
        print('发现多台设备:')

        for i in range(num_devices):
            print(i, LockdownClient(device_list[i].serial).all_values['DeviceName'])

        index = int(input('请输入对应数字以选择设备: '))
        device = device_list[index]

    device = device_list[index]
    device_lockdown_client = LockdownClient(device.serial)

    device_info = device_lockdown_client.all_values
    device_class = device_info['DeviceClass']
    ios_version = device_info['ProductVersion'][0:4]
    device_name = device_info['DeviceName']

    print(f'已连接到您的{device_class}: {device_name}, 系统版本为{ios_version}')
    print('请确保在镜像挂载完成之前手机已解锁且屏幕亮起。')

    ios_version_replace = {'14.8': '14.7', '15.1': '15.0'}
    if ios_version in ios_version_replace:
        ios_version = ios_version_replace[ios_version]

    result = image.mount_image(device_lockdown_client, ios_version)
    if result == 0:
        return

    location_simulator = DtSimulateLocation(lockdown=device_lockdown_client)

    # 生成记录
    points = gen_record(distance, speed)

    dur_time = timedelta(seconds=round(points[-1][-1]))
    curr_time = datetime.now().replace(microsecond=0)

    print(f"""
跑步开始：
  总里程：\t{distance}米
  平均配速：\t{speed // 60}分{speed % 60}秒 每公里
  总时长：\t{dur_time}
  开始时间：\t{curr_time}
  结束时间：\t{dur_time + curr_time}（预计）
    """)

    asyncio.run(auto_run(points, location_simulator))

    print('跑步完成, 请在手机上结束跑步，建议清除定位。')
    print('· 输入 0 以清除定位但不重启设备；')
    print('· 输入 1 以清除定位并且重启设备；')
    print('· 如果什么也不做，可以直接退出程序，')
    print('  请注意这种情况下定位会被保留在最后一次的位置。')

    arg = input()
    if arg == '0':
        location_simulator.clear()
        image.unmount_image(device_lockdown_client)
    elif arg == '1':
        DiagnosticsService(device_lockdown_client).restart()

    return


if __name__ == '__main__':
    print(r'''
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|
''')
    print('\nPKUAutoRun v1.1.0')
    print('提示: 如果要使用多台设备同时打卡, 请多开本程序')

    _distance = int(input('请输入跑步里程(米), 如5公里输入5000: '))
    if _distance < 1000:
        print('警告：里程不符合要求')

    _speed = int(input('请输入你希望的平均配速(秒), 如五分配速输入300: '))
    if not 240 < _speed < 600:
        print('警告：配速不符合要求')

    # 如果在 Python 脚本中运行程序，可以直接在下面修改路径使用：
    # _distance = 10000
    # _speed = 280
    main(_distance, _speed)
