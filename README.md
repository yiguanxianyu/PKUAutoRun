# PKUAutoRun

或许是一种可以偷懒的方法。

PKUAutoRun 是一个顾名思义的工具。它针对的是 iOS 平台。不过针对其他平台，这里也给出了一些相应的建议。目前你只能通过在手机上观察并在适当的时间手动结束。程序所模拟的轨迹来自于真实跑步的记录，所以需要更多的补充。

#### 待做的功能

- [ ] 显示剩余的时间
- [ ] ···

## 可能的方案

- 如果你使用安卓手机（包括鸿蒙）且已经 root （如果你不知道 root 是什么，那就是没有）

  ​		FakeLocation
  
- 如果你使用安卓手机（包括鸿蒙）但没有 root

    - 你使用 Windows 系统

        安卓模拟器 + FakeLocation

    - 你使用 macOS/Linux 并且使用 PKURunner

        PKUNoRun

    - 你使用 macOS/Linux 并且使用乐动力

        安卓模拟器 + FakeLocation

- 如果你使用 iPhone/iPad

    - 你使用 Windows 系统

        PKUAutoRun 或 FakeLocation

    - 你使用 macOS

        PKUAutoRun

    - 你使用 Linux

        安卓模拟器 + FakeLocation



PKUNoRun参见：[PKUNoRun](https://github.com/PKUNoRun/PKUNoRun)

FakeLocation 需要氪金使用（但不贵），详情参见 [Android.pdf](https://github.com/yiguanxianyu/PKUAutoRun/blob/main/Android.pdf)

## 用法

1. 下载 [iTunes](https://www.apple.com.cn/itunes/) 64位版并安装（仅限 Windows 用户）。你可以直接[点击这里](https://www.apple.com/itunes/download/win64)下载，不要使用 Microsoft Store 版本的 iTunes ；

2. 安装 [Python3](https://www.python.org/)。建议使用 Python 3.9 及更新的版本，你也可以在其他的版本上自行测试；

3. 安装程序运行所需的依赖包：

     `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

4. 将你的 iOS 设备通过 USB 端口连接到电脑；

5. 解锁设备，选择信任此电脑，并保持屏幕亮起；

6. 在手机上开始跑步；

7. 运行 `main.py`。

## Q&A

1. 发生了`[WinError 10053]`错误： 

    请检查挂载镜像时屏幕是否亮起。

2. 如果中途需要关闭程序或者拔掉手机怎么办？

   请先手动结束跑步。这之后，你需要通过手动重启来恢复原本的定位。方法：`设置->通用->拉到最底->关机`。