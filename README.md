# PKUAutoRun

或许是一种可以偷懒的方法。**目前仍在开发中，** 如果有各种问题欢迎提 issue。~~来个人试用一下吧求求了~~

PKUAutoRun 是一个顾名思义的工具。它面向 iOS/iPadOS，可以在 macOS 和 Windows 中运行（Linux 由于缺少 iTunes 驱动而无法使用）。通过 PKUAutoRun ，你甚至可以使用 iPad 完成跑步打卡（这是否略显赛博朋克）。然而，如果你并不使用 iPhone 或者 iPad ，就无法直接使用这个项目。不过针对其他平台，[这里](https://github.com/yiguanxianyu/PKUAutoRun#可能的方案)也给出了一些相应的建议。

目前你只能通过在手机上观察并在适当的时间手动结束。程序所模拟的轨迹来自于真实跑步的记录，所以需要更多的补充，欢迎你上传自己的跑步记录造福大家。具体方法见 [Q&A](https://github.com/yiguanxianyu/PKUAutoRun#qa)。

由于学业原因，此项目无法频繁更新，因此更丰富的功能可能短期内不会出现。不过现在的版本已经足够你进行跑步打卡了。 

**待做的功能**

- [ ] 显示剩余的时间
- [ ] 为已有的轨迹加入随机的漂移
- [ ] ~~使用程序生成随机的轨迹进行跑步打卡。~~ 此项原本在计划中，然而由于本人时间精力有限，暂时没有办法去做了。

## 用法

0. 提示：iOS 15.3/15.3.1 的用户可能会遭遇无法使用的问题，你可能需要将设备升级至 15.4 或者更新的版本以解决此问题。

1. Windows 用户下载 [iTunes](https://www.apple.com.cn/itunes/) 64位版并安装。你可以直接[点击这里](https://www.apple.com/itunes/download/win64)下载，不要使用 Microsoft Store 版本的 iTunes；

2. 安装 [Python3](https://www.python.org/)。建议使用 Python 3.9 及更新的版本，你也可以在其他的版本上自行测试。你还可以尝试[打包好的程序](https://github.com/yiguanxianyu/PKUAutoRun/releases/latest)，这可以帮你省去安装 Python 和依赖包的工作，不过并不能保证完整的可用性；

3. 安装程序运行所需的依赖包：

    `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

4. 将你的 iOS 设备通过 USB 端口连接到电脑；

5. 解锁设备，选择信任此电脑，并保持屏幕亮起；

5. 关闭打卡软件除了定位和网络以外的所有权限；

6. 在 `main.py` 中修改你要使用的 GPX 文件路径；

7. 运行 `main.py`；

8. 在手机上开始跑步，这之后你可以让手机屏幕自动关闭。

## Q&A

1. 发生了`[WinError 10053]`错误： 

   请检查挂载镜像时屏幕是否亮起。

2. 如果中途需要关闭程序或者拔掉手机怎么办？

   请先手动结束跑步。这之后，你需要通过手动重启来恢复原本的定位。方法：`设置 -> 通用-> 拉到最底 -> 关机`。

3. 我如何记录自己的数据？

   - 如果你有 Apple Watch ，你可以在乐动力/PKURunner上开始跑步的同时使用体能训练 App 记录你的运动信息，跑步结束后你可以在 iPhone 的健身 App — 体能训练中看到这次运动记录。进入`健康 — 摘要`，点击头像，然后拉到最底，选择`导出所有健康数据`。将导出的 zip 文件传至电脑上解压。在 workout-routes 文件夹内，你可以看到已导出的 GPX 文件。
   - （推荐）你可以在 App Store 下载 `Open GPX Tracker` ，在跑步时和乐动力/PKURunner同时使用并记录轨迹。

4. 我如何上传自己的数据造福人类？

   你可以直接发起 Pull Request 。如果你不知道如何发起 PR ，也可以将你的 GPX 文件发送至 yiguanxianyu@protonmail.com ，由我上传数据。

## 可能的方案

- 如果你使用安卓手机（包括鸿蒙）且已经 root （如果你不知道 root 是什么，那就是没有）

    FakeLocation

- 如果你使用安卓手机（包括鸿蒙）但没有 root

    - 你使用 Windows

        安卓模拟器 + FakeLocation

    - 你使用 macOS/Linux 并且使用 PKURunner

        PKUNoRun

    - 你使用 Linux 并且使用乐动力

        安卓模拟器 + FakeLocation

    - 你使用 macOS 并且使用乐动力

        求求你不要用这么阴间的组合

- 如果你使用 iPhone/iPad

    - 你使用 Windows

        PKUAutoRun 或 安卓模拟器 + FakeLocation

    - 你使用 macOS

        PKUAutoRun

    - 你使用 Linux

        安卓模拟器 + FakeLocation

请注意：

- 我并不了解 Linux 安卓模拟器的工作情况，建议不要使用（应该不会有人只使用 GNU/Linux 吧）。
- 本程序不保证能够在虚拟机中正常工作，有需要请自行尝试。

PKUNoRun参见：[PKUNoRun](https://github.com/PKUNoRun/PKUNoRun)

FakeLocation 需要氪金使用（但不贵），详情参见 [Android.pdf](https://github.com/yiguanxianyu/PKUAutoRun/blob/main/Android.pdf)

## 写在最后

当然，我还是希望大家能够自己去跑一跑步的。毕竟，健康也很重要嘛。