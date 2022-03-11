# PKUAutoRun

**开发中**

或许是一种可以偷懒的方法。

可能的方案：

- 如果你使用安卓手机且已经 root
  如果你不知道 root 是什么，那就是没有

  FakeLocation 
  
- 如果你使用安卓手机但没有 root

    - 你使用 Windows 系统

        安卓模拟器 + FakeLocation

    - 你使用 macOS/Linux 并且使用 PKURunner

        PKUNoRun

    - 你使用 macOS/Linux 并且使用乐动力

        弃疗

- 如果你使用 iPhone/iPad

    - 你使用 Windows 系统

        PKUAutoRun 或 FakeLocation

    - 你使用 macOS

        PKUAutoRun

    - 你使用 Linux

        放弃治疗

PKUNoRun参见：[PKUNoRun](https://github.com/PKUNoRun/PKUNoRun)

FakeLocation 的用法参见 [Android.pdf](https://github.com/yiguanxianyu/PKUAutoRun/blob/main/Android.pdf)

## 用法

1. 下载 [iTunes](https://www.apple.com.cn/itunes/) 64位版并安装（仅限 Windows 用户）；

2. 安装 Python3. 已知 Python3.9 可以正常运行，但其他版本未做测试。建议使用 Python3.7 及更新的版本；

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