# PKUAutoRun

赛博跑步机，或许是一种可以偷懒的方法，也或许不能，但请使用乐动力。**请使用者自行承担后果。 暂不支持iOS17**

当前版本 v1.2.1 (2023-02-20)，[更新日志](https://github.com/yiguanxianyu/PKUAutoRun/blob/main/CHANGELOG.md)。如果有各种问题欢迎提 issue。~~真的不来尝试一下吗\~~~

PKUAutoRun 是一个顾名思义的工具。它面向 iOS/iPadOS，支持 Windows/macOS/Linux（Linux 平台未经测试）。通过 PKUAutoRun ，你甚至可以使用 iPad 完成跑步打卡。然而，如果你并不使用 iPhone/iPad/iPod ，那就无法直接使用这个项目。由于本程序所依赖的项目仍在积极开发中，如果你在运行过程中遇到任何问题，请先考虑再运行一次程序。

### 重要：iOS 16 请阅读下文

在 iOS 16 中，Apple 修改了开发者模式的逻辑，现在你需要一些额外的操作才能够开启开发者模式以使用 PKUAutoRun。

- 推荐方案

  - 请下载并安装 [爱思助手](https://www.i4.cn/)，在工具箱中找到虚拟定位模块，随意选择一个地址并确定，按照提示打开开发者模式。

- 可选方案

  - 使用已经安装了 Xcode 的 Mac 电脑，打开 Xcode 随意新建一个 Swift 项目，并将设备连接到 Mac。在 `设置-隐私与安全性-安全性` 中找到并打开开发者模式。
  - 如果不愿或无法使用推荐方案，你需要关闭设备密码再运行脚本，脚本会自动为你开启开发者模式。在运行完程序后，你可以再打开密码，此时开发者模式将立即失效，你需要手动重启设备并重新激活开发者模式。

**功能**

- [X] 自定义配速
- [X] 多设备支持（多开）
- [X] 由程序生成的随机跑步记录（参见[鸣谢](https://github.com/yiguanxianyu/PKUAutoRun#鸣谢)）

## 用法

0. 如果你看不懂下面的说明，可以找一位工具人代劳。

1. Windows 用户下载 [爱思助手](https://www.i4.cn/)（推荐）或 [iTunes64位版](https://www.apple.com/itunes/download/win64) 并安装。**不要使用 Microsoft Store 版本的 iTunes**。本项目只依赖 iTunes 中的 Apple Mobile Device Support，所以如果你用不到其他的模块话可以卸载掉 Apple Software Update, Bonjour 和 iTunes 本体.

2. 安装 [Python3](https://www.python.org/)。支持 `Python 3.6+` ；

3. 下载本项目代码，并安装程序运行所需的依赖包（推荐使用虚拟环境）：
    
    ```
    $ pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

4. 将你的设备通过 USB 端口连接到电脑；

5. 解锁设备，选择信任此电脑，并保持屏幕亮起；

5. 关闭打卡软件除了定位和网络以外的所有权限；

6. 运行 `main.py`，并设定相关配置；

7. 在打卡软件中开始跑步，这之后你可以让设备屏幕自动关闭。

## Q&A

1. 发生了`[WinError 10053]`错误： 

   请检查挂载镜像时屏幕是否亮起。

2. 下载镜像长时间没有反应：

   关掉梯子再运行程序。

3. 如果中途需要关闭程序或者拔掉手机怎么办？

   请先手动结束跑步。这之后，你需要通过手动重启来恢复原本的定位。方法：`设置 -> 通用 -> 拉到最底 -> 关机`。

4. 我的运动步数为 0 ？

   由于苹果对于开发者的限制，iOS 只支持模拟定位，而不支持模拟以下内容：定位误差、海拔及其误差、航向、速度、步数等。对于乐动力来说可以通过关闭健康权限的方式避免计步从而绕过这个问题。目前来看这一点并不影响使用。

## 鸣谢

感谢 [@yuchenxi2000](https://github.com/yuchenxi2000) 在 https://github.com/PKUNoRun/PKUNoRun/issues/17 中提供的跑步记录生成器

## 写在最后

当然，我还是希望大家能够自己去跑一跑步的。毕竟，健康也很重要嘛。
