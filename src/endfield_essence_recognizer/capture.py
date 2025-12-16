"""窗口截图和区域捕获工具模块。"""

import logging
from ctypes import byref, windll, wintypes

import cv2
import numpy as np
import win32con
import win32gui
import win32ui


def get_client_rect_screen(hwnd: int) -> tuple[int, int, int, int]:
    """
    获取窗口客户区在屏幕上的位置和大小。

    Args:
        hwnd: 窗口句柄

    Returns:
        (left, top, width, height) 元组，表示客户区的屏幕坐标和尺寸
    """
    rect = wintypes.RECT()
    windll.user32.GetClientRect(hwnd, byref(rect))
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    point = wintypes.POINT(rect.left, rect.top)
    windll.user32.ClientToScreen(hwnd, byref(point))

    return point.x, point.y, width, height


# def get_client_rect_screen(hwnd: int) -> tuple[int, int, int, int]:
#     """另一个实现，使用 win32gui"""
#     left, top = win32gui.ClientToScreen(hwnd, (0, 0))
#     cr = win32gui.GetClientRect(hwnd)
#     right, bottom = win32gui.ClientToScreen(hwnd, (cr[2], cr[3]))
#     width = right - left
#     height = bottom - top
#     return left, top, width, height


def screenshot(rect: tuple[int, int, int, int]) -> np.ndarray | None:
    """
    截取屏幕指定区域，返回 BGR 格式的 numpy 图像。

    Args:
        rect: 矩形区域 (left, top, right, bottom) 的屏幕坐标

    Returns:
        numpy 数组（BGR 格式，OpenCV 兼容）
    """
    left, top, right, bottom = rect
    width, height = right - left, bottom - top
    if width <= 0 or height <= 0:
        return None

    # 创建设备上下文和位图
    screen_dc = win32gui.GetDC(0)
    img_dc = win32ui.CreateDCFromHandle(screen_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(bitmap)

    # 复制屏幕区域到位图
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    # 读取位图像素数据
    bmpinfo = bitmap.GetInfo()
    bpp = bmpinfo["bmBitsPixel"] // 8  # 每像素字节数（通常为3或4）
    stride = ((width * bpp + 3) // 4) * 4  # 4字节对齐的行宽
    raw = bitmap.GetBitmapBits(True)

    # 转换为 numpy 数组
    arr = np.frombuffer(raw, dtype=np.uint8)
    arr = arr.reshape((height, stride))
    arr = arr[:, : width * bpp]  # 移除对齐填充
    arr = arr.reshape((height, width, bpp))

    # 如果是 BGRA 格式，转换为 BGR
    if bpp == 4:
        arr = arr[:, :, :3]  # 丢弃 alpha 通道

    # 释放 GDI 资源
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(0, screen_dc)
    win32gui.DeleteObject(bitmap.GetHandle())

    return arr.copy()


def capture_client_roi_np(
    hwnd: int, rect: tuple[int, int, int, int]
) -> np.ndarray | None:
    """
    抓取窗口客户区内指定 ROI 区域，返回 BGR 格式的 numpy 图像。

    此函数用于在内存中直接获取屏幕区域的像素数据，无需保存文件，
    适合实时图像识别场景。

    Args:
        hwnd: 窗口句柄
        rect: ROI 矩形，使用客户区像素坐标 (x1, y1, x2, y2)
            - x1, y1: 左上角坐标（相对于客户区左上角）
            - x2, y2: 右下角坐标（相对于客户区左上角）

    Returns:
        numpy 数组（BGR 格式，OpenCV 兼容）

    技术细节：
        - 将客户区坐标转换为屏幕坐标
        - 使用 GDI BitBlt 复制屏幕区域
        - 读取位图原始字节并转换为 numpy 数组
        - 处理字节对齐（stride）和颜色通道顺序
        - 自动丢弃 alpha 通道（如果存在）
    """
    x1, y1, x2, y2 = rect
    if x2 <= x1 or y2 <= y1:
        return None

    # 计算屏幕绝对坐标
    left, top, _, _ = get_client_rect_screen(hwnd)
    abs_left = left + x1
    abs_top = top + y1
    abs_right = left + x2
    abs_bottom = top + y2

    # 调用 screenshot 函数获取屏幕区域
    return screenshot((abs_left, abs_top, abs_right, abs_bottom))
