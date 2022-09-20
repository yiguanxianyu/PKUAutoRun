# PKUAutoRun

赛博跑步机，或许是一种可以偷懒的方法，也或许不能。

当前版本 v1.1.0 (2022-09-21)，[更新日志](https://github.com/yiguanxianyu/PKUAutoRun/blob/main/CHANGELOG.md)。如果有各种问题欢迎提 issue。~~真的不来尝试一下吗\~~~

PKUAutoRun 是一个顾名思义的工具。它面向 iOS/iPadOS，支持 Windows/macOS/Linux（Linux 平台未经测试）。通过 PKUAutoRun ，你甚至可以使用 iPad 完成跑步打卡（尽显赛博本色）。然而，如果你并不使用 iPhone/iPad/iPod ，那就无法直接使用这个项目。

**请使用者自行承担后果**

**功能**

- [X] 自定义配速
- [X] 多设备支持（多开）
- [X] 由程序生成的随机跑步记录（参见[鸣谢](https://github.com/yiguanxianyu/PKUAutoRun#鸣谢)）

## 用法

0. 如果你看不懂下面的说明，可以找一位工具人代劳。

1. Windows 用户下载 [iTunes](https://www.apple.com.cn/itunes/) 64位版并安装。你可以直接[点击这里](https://www.apple.com/itunes/download/win64)下载，**不要使用 Microsoft Store 版本的 iTunes**；

2. 安装 [Python3](https://www.python.org/)。支持 `Python 3.6+` ；

3. 下载本项目代码，并安装程序运行所需的依赖包：
    
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
