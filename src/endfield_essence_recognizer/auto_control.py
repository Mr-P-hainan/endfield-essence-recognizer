"""
终末地自动化控制脚本
功能：
- 按"["键：对终末地窗口截图并保存
- 按"]"键：持续点击终末地窗口正中间，再次按"]"键中断
- 按Alt+Delete：退出程序
"""

import threading
import time
from datetime import datetime
from pathlib import Path

import keyboard
import numpy as np
import pyautogui
import pygetwindow
import win32gui

from endfield_essence_recognizer.image import (
    linear_operation,
    load_image,
    save_image,
    scope_to_slice,
)
from endfield_essence_recognizer.log import logger
from endfield_essence_recognizer.screenshot import (
    get_client_rect,
    get_client_rect_screen_by_ctypes,
    get_client_rect_screen_by_win32gui,
    screenshot_by_pyautogui,
    screenshot_by_win32ui,
    screenshot_window,
)

# 全局变量
clicking = False
running = True
screenshot_dir = Path("screenshots")

# 基质图标位置网格（客户区像素坐标）
# 9列5行，共45个图标位置
essence_icon_x_list = np.linspace(128, 1374, 9).astype(int)
essence_icon_y_list = np.linspace(196, 819, 5).astype(int)
icon_pos_grid = np.array(
    [(x, y) for y in essence_icon_y_list for x in essence_icon_x_list]
)


def find_window(title_keyword="EndfieldTBeta2") -> pygetwindow.Window | None:
    """查找包含指定关键词的窗口"""
    try:
        windows = pygetwindow.getWindowsWithTitle(title_keyword)
        if windows:
            return windows[0]
        return None
    except Exception as e:
        logger.error(f"查找窗口时出错: {e}")
        return None


def auto_click_icons():
    """循环点击icon_pos_grid中的坐标，每次点击后截一张图（不保存）。"""
    global clicking

    window = find_window()
    if window is None:
        logger.error("未找到终末地窗口！")
        clicking = False
        return

    try:
        if window.isMinimized:
            window.restore()
        window.activate()
        time.sleep(0.1)

        logger.info("开始依次点击icon_pos_grid坐标并截屏...")
        while clicking and running:
            # 获取窗口客户区屏幕坐标，用于将客户端坐标转换为屏幕坐标
            client_rect = get_client_rect(window)
            if client_rect is None:
                logger.error("无法获取窗口客户区坐标，停止点击")
                clicking = False
                break

            client_left = client_rect["left"]
            client_top = client_rect["top"]

            for rel_x, rel_y in icon_pos_grid:
                if not clicking or not running:
                    break

                screen_x = client_left + rel_x
                screen_y = client_top + rel_y

                # 点击坐标（icon_pos_grid坐标是相对客户区左上角，需要转成屏幕坐标）
                pyautogui.click(screen_x, screen_y)

                # 截取当前窗口图像（结果暂不使用）
                try:
                    _ = screenshot_window(window)
                except Exception:
                    pass

                time.sleep(0.05)
    except Exception as e:
        logger.error(f"自动点击失败: {e}")
        clicking = False


def on_bracket_left():
    """处理 "[" 键按下事件 - 截图"""
    window = find_window()
    if window and window.isActive:
        logger.info("检测到'['键，开始截图...")
        image = screenshot_window(window)
        timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
        filename = screenshot_dir / f"screenshot_{timestamp}.png"
        save_image(image, filename)
        logger.info(f"截图已保存到: {filename}")


def on_bracket_right():
    """处理 "]" 键按下事件 - 切换自动点击"""
    global clicking

    window = find_window()
    if window and window.isActive:
        clicking = not clicking

        if clicking:
            logger.info("检测到 ']' 键，开始依次点击 icon_pos_grid...")
            # 在新线程中启动自动点击
            click_thread = threading.Thread(target=auto_click_icons, daemon=True)
            click_thread.start()
        else:
            logger.info("检测到 ']' 键，停止自动点击")


def on_exit():
    """处理 Alt+Delete 按下事件 - 退出程序"""
    global running, clicking
    logger.info("检测到 Alt+Delete，退出程序...")
    clicking = False
    running = False


def main():
    """主函数"""
    global running

    logger.success(
        "\n"
        + "=" * 50
        + "\n"
        + "终末地自动化控制脚本已启动\n"
        + "\n"
        + "=" * 50
        + "\n"
        + "功能说明：\n"
        + "  [键：对终末地窗口截图并保存\n"
        + "  ]键：开始/停止持续点击窗口中心\n"
        + "  Alt+Delete：退出程序\n"
        + "=" * 50
    )
    logger.info("等待终末地窗口...")

    # 等待终末地窗口出现
    while running:
        window = find_window()
        if window:
            logger.info(f"已找到窗口: {window.title}")
            break
        time.sleep(1)

    if not running:
        return

    logger.info("开始监听热键...")

    # 注册热键
    keyboard.add_hotkey("[", on_bracket_left)
    keyboard.add_hotkey("]", on_bracket_right)
    keyboard.add_hotkey("alt+delete", on_exit)

    # 保持程序运行
    try:
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("程序被中断")
    finally:
        # 清理
        keyboard.unhook_all()
        logger.info("程序已退出")


if __name__ == "__main__":
    main()
