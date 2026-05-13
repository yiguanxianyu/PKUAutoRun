# -*- coding:utf-8 -*
import asyncio
from datetime import datetime, timedelta

import compat_pymobiledevice3  # noqa: F401 — 须在其它 pymobiledevice3 导入之前（见该文件说明）

from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.services.simulate_location import DtSimulateLocation
from pymobiledevice3.usbmux import list_devices

import image
from gen_record import gen_record
import terminal_ui as ui


async def auto_run(points, location_simulator):

    async def set_loc(lat, lon, t):
        await asyncio.sleep(t)
        location_simulator.set(lat, lon)

    await asyncio.gather(*(set_loc(*p) for p in points))


def main(distance, speed):
    ui.setup()
    device_list = list_devices()
    if not device_list:
        ui.subtitle('未找到设备')
        ui.bullet('是否已下载并安装 iTunes（或爱思助手）')
        ui.bullet('是否已将设备连接到电脑、解锁并勾选「信任此电脑」')
        input(ui.dim('按下回车退出… '))
        return

    num_devices = len(device_list)
    index = 0

    if num_devices > 1:
        ui.subtitle('多台设备')
        for i in range(num_devices):
            name = LockdownClient(device_list[i].serial).all_values['DeviceName']
            print(ui.dim(f'  [{i}]  ') + name)
        index = int(input(ui.cyan('请输入设备序号: ')))

    device = device_list[index]
    device_lockdown_client = LockdownClient(device.serial)

    device_info = device_lockdown_client.all_values
    device_class = device_info['DeviceClass']
    ios_version = device_info['ProductVersion'][0:4]
    device_name = device_info['DeviceName']

    print()
    print(ui.green(f'  已连接  {device_class}  ·  {device_name}'))
    print(ui.dim(f'  iOS {ios_version}'))
    print(ui.yellow('  挂载镜像时请保持手机解锁、屏幕亮起。'))

    ios_version_replace = {
        '14.8': '14.5',
        '15.1': '15.0',
        '15.3': '15.2',
        '15.8': '15.7',  # 镜像源无 15.8 目录，下载会得到 404，设备端报 ReceiveBytes / signature 错误
        '16.2': '16.1',
        '16.3': '16.1',
        '16.6': '16.5',
        '16.7': '16.5',
    }
    if ios_version in ios_version_replace:
        ios_version = ios_version_replace[ios_version]

    try:
        result = image.mount_image(device_lockdown_client, ios_version)
    except Exception as e:
        if "'Error': 'DeviceLocked'" in str(e):
            print(ui.red('设备已锁定，请先解锁手机。'))
        else:
            print(ui.red(str(e)))
        return
    if result == 0:
        return

    # 生成记录
    points = gen_record(distance, speed)
    dur_time = timedelta(seconds=round(points[-1][-1]))
    curr_time = datetime.now().replace(microsecond=0)

    ui.subtitle('跑步参数')
    lines = [
        f'总里程　　 {distance} 米',
        f'平均配速　 {speed // 60} 分 {speed % 60} 秒 / 公里',
        f'总时长　　 {dur_time}',
        f'开始时间　 {curr_time}',
        f'预计结束　 {dur_time + curr_time}',
    ]
    for line in lines:
        print(ui.dim('  ') + line)
    ui.hr()
    print()

    ui.subtitle('跑步进行中')
    print(ui.dim('  模拟定位已启动，请在手机上开始跑步。'))
    print()

    location_simulator = DtSimulateLocation(lockdown=device_lockdown_client)
    asyncio.run(auto_run(points, location_simulator))

    ui.subtitle('跑步完成')
    print(ui.dim('  请在手机上结束跑步。定位清理：'))
    ui.bullet(ui.cyan('0') + ui.dim(' — 清除定位并卸载开发者镜像（推荐）'))
    ui.bullet(ui.cyan('1') + ui.dim(' — 清除定位并重启手机'))
    ui.bullet(ui.dim('直接回车 — 保留当前模拟位置后退出'))
    print()

    arg = input(ui.cyan('请输入选项后回车: '))
    if arg == '0':
        location_simulator.clear()
        image.unmount_image(device_lockdown_client)
    elif arg == '1':
        DiagnosticsService(device_lockdown_client).restart()


if __name__ == '__main__':
    ui.setup()
    _banner = r'''
  _____  _  ___    _              _        _____
 |  __ \| |/ / |  | |  /\        | |      |  __ \
 | |__) | ' /| |  | | /  \  _   _| |_ ___ | |__) |   _ ____
 |  ___/|  < | |  | |/ /\ \| | | | __/ _ \|  _  / | | |  _  \
 | |    | . \| |__| / ____ \ |_| | || (_) | | \ \ |_| | | | |
 |_|    |_|\_\_____/_/    \_\____|\__\___/|_|  \_\____|_| |_|
'''.strip('\n')
    for _line in _banner.split('\n'):
        print(ui.cyan(_line))
    print()
    print(ui.brand('PKUAutoRun'), ui.dim('v1.2.1'))
    print(ui.dim('多台设备请多开窗口分别运行。'))
    print()

    _distance = int(input(ui.cyan('跑步里程（米，如 5000）: ')))
    if _distance < 1000:
        print(ui.yellow('  警告：里程低于 1000 米可能不符合要求'))

    _speed = int(input(ui.cyan('平均配速（秒/公里，如 300 表示五分）: ')))
    if not 240 < _speed < 600:
        print(ui.yellow('  警告：配速建议在 240～600 秒/公里之间'))

    # 如果在 Python 脚本中运行程序，可以直接在下面修改参数使用：
    # _distance = 10000
    # _speed = 280
    main(_distance, _speed)
