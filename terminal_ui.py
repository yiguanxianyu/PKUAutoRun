# -*- coding: utf-8 -*-
"""
终端输出美化：无第三方依赖；在 Windows 10+ 控制台尝试开启 ANSI 颜色。
若环境不支持颜色，自动降级为纯文本。
"""
from __future__ import annotations

import sys

_OK = False

# ANSI（需终端支持；Windows 需开启虚拟终端处理）
_RESET = '\033[0m'
_BOLD = '\033[1m'
_DIM = '\033[2m'
_CYAN = '\033[36m'
_GREEN = '\033[32m'
_YELLOW = '\033[33m'
_RED = '\033[31m'
_GRAY = '\033[90m'


def setup() -> None:
    """在程序尽早处调用一次。"""
    global _OK
    _OK = False
    if not sys.stdout.isatty():
        return
    if sys.platform == 'win32':
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING
            if kernel32.SetConsoleMode(handle, mode.value | 0x0004):
                _OK = True
        except Exception:
            _OK = False
    else:
        _OK = True


def _wrap(text: str, *prefix: str) -> str:
    if not _OK or not prefix:
        return text
    return ''.join(prefix) + text + _RESET


def bold(text: str) -> str:
    return _wrap(text, _BOLD)


def dim(text: str) -> str:
    return _wrap(text, _DIM, _GRAY)


def cyan(text: str) -> str:
    return _wrap(text, _CYAN)


def green(text: str) -> str:
    return _wrap(text, _GREEN)


def yellow(text: str) -> str:
    return _wrap(text, _YELLOW)


def red(text: str) -> str:
    return _wrap(text, _RED)


def brand(text: str) -> str:
    """加粗 + 青色，用于标题。"""
    return _wrap(text, _BOLD, _CYAN)


def hr(width: int = 48, char: str = '─') -> None:
    line = char * width
    print(dim(line) if _OK else line)


def subtitle(text: str) -> None:
    print()
    hr()
    print(bold(cyan(f' {text} ')))
    hr()


def bullet(text: str) -> None:
    print(dim('  · ') + text)
