from __future__ import print_function

import ctypes
from ctypes import wintypes
from collections import namedtuple
import time


def GetWindowRectFromName(name: str) -> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    # print(hwnd)
    # print(rect)
    return (rect.left, rect.top, rect.right, rect.bottom)
