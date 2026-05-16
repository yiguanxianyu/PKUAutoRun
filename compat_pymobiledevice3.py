# -*- coding: utf-8 -*-
"""
pymobiledevice3 1.42.4 与新版 construct（随 Python 3.12+ 常见）的兼容补丁。

construct 2.10+ 在 parse_stream 中会调用 stream.tell()，而 1.42.4 的 SafeStreamSocket
未实现 tell()。把 construct 锁在 <2.10 在 Python 3.13 上不可行（依赖已移除的 imp）。

用法：在导入任何其他 pymobiledevice3 子模块之前执行::

    import compat_pymobiledevice3  # noqa: F401

若将来升级到 pymobiledevice3 9.x（async API），应删除本模块并改写业务代码，而不是继续补丁。
"""
import pymobiledevice3.usbmux as _pymd3_usbmux

_base = _pymd3_usbmux.SafeStreamSocket


class _SafeStreamSocketWithTell(_base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._construct_stream_pos = 0

    def tell(self):
        return self._construct_stream_pos

    def recv(self, size: int) -> bytes:
        data = super().recv(size)
        self._construct_stream_pos += len(data)
        return data


_pymd3_usbmux.SafeStreamSocket = _SafeStreamSocketWithTell
