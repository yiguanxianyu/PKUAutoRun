# PKUAutoRun

**开发中**

或许是一种可以偷懒的方法。

Windows/安卓氪金用户请参照 Android.pdf 文件，iOS用户/无Windows用户请耐心等待。Linux用户请参照[PKUNoRun](https://github.com/PKUNoRun/PKUNoRun)

## 用法

1. 下载 [iTunes](https://www.apple.com.cn/itunes/) 64位版并安装（仅限 Windows 用户）；

2. 安装 Python3. 已知 Python3.9 可以正常运行，但其他版本未做测试。建议使用 Python3.7 及更新的版本；

3. 安装程序运行所需的环境：

    在项目目录下新建虚拟环境，并安装 `requirements.txt`

4. 将你的 iOS 设备通过 USB 端口连接到电脑；

5. 解锁设备，选择信任此电脑，并保持屏幕亮起

6. 在手机上开始跑步

7. 运行 `main.py`

## Q&A

1. 发生了`[WinError 10053]`错误： 

    请检查挂载镜像时屏幕是否亮起。

2. 如果中途需要关闭程序或者拔掉手机怎么办？

   请先手动结束跑步。这之后，你需要通过手动重启来恢复原本的定位。方法：`设置->通用->拉到最底->关机`。