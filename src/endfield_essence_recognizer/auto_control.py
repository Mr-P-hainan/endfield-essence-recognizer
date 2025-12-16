"""
终末地自动化控制脚本
功能：
- 按 "[" 键：对终末地窗口截图并保存
- 按 "]" 键：持续点击终末地窗口正中间，再次按 "]" 键中断
- 按 Alt+Delete：退出程序
"""

from __future__ import annotations

import threading
import time
import warnings
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
from endfield_essence_recognizer.recognizer import Recognizer
from endfield_essence_recognizer.screenshot import (
    get_client_rect,
    get_client_rect_screen_by_ctypes,
    get_client_rect_screen_by_win32gui,
    screenshot_by_pyautogui,
    screenshot_by_win32ui,
    screenshot_window,
)

enable_sound_path = Path("sounds/enable.wav")
disable_sound_path = Path("sounds/disable.wav")
supported_window_titles = ["EndfieldTBeta2"]

# 全局变量
running = True
click_thread: EssenceScanner | None = None
screenshot_dir = Path("screenshots")

# 基质图标位置网格（客户区像素坐标）
# 5 行 9 列，共 45个 图标位置
essence_icon_x_list = np.linspace(128, 1374, 9).astype(int)
essence_icon_y_list = np.linspace(196, 819, 5).astype(int)
icon_pos_grid = np.array(
    [(x, y) for y in essence_icon_y_list for x in essence_icon_x_list]
)

ATTRIBUTE_STATS_ROI = (1508, 358, 1700, 390)
SECONDARY_STATS_ROI = (1508, 416, 1700, 448)
SKILL_STATS_ROI = (1508, 468, 1700, 500)
all_attribute_stats = ["敏捷提升", "力量提升", "意志提升", "智识提升", "主能力提升"]
all_secondary_stats = [
    "攻击提升",
    "生命提升",
    "物理伤害提升",
    "灼热伤害提升",
    "电磁伤害提升",
    "寒冷伤害提升",
    "自然伤害提升",
    "暴击率提升",
    "源石技艺提升",
    "终结技效率提升",
    "法术伤害提升",
    "治疗效率提升",
]
all_skill_stats = [
    "强攻",
    "压制",
    "追袭",
    "粉碎",
    "昂扬",
    "巧技",
    "残暴",
    "附术",
    "医疗",
    "切骨",
    "迸发",
    "夜幕",
    "流转",
    "效益",
]
recognizer = Recognizer(
    labels=all_attribute_stats + all_secondary_stats + all_skill_stats,
    templates_dir=Path("templates"),
)


def get_active_support_window() -> pygetwindow.Window | None:
    active_window = pygetwindow.getActiveWindow()
    if active_window is not None and active_window.title in supported_window_titles:
        return active_window
    else:
        return None


class EssenceScanner(threading.Thread):
    """
    基质图标扫描器后台线程。

    此线程负责自动遍历游戏界面中的 45 个基质图标位置，
    对每个位置执行"点击 -> 截图 -> 识别"的流程。

    属性：
        scanning: 当前是否正在扫描
        _stop: 线程停止事件
        _interrupt: 扫描中断事件
    """

    def __init__(
        self,
    ) -> None:
        super().__init__(daemon=True)
        self._scanning = threading.Event()

    def run(self) -> None:
        logger.info("开始依次点击 icon_pos_grid 坐标并截屏...")
        self._scanning.set()
        for rel_x, rel_y in icon_pos_grid:
            window = get_active_support_window()
            if window is None:
                logger.info("终末地窗口不在前台，停止基质扫描。")
                self._scanning.clear()
                break

            if not self._scanning.is_set():
                logger.info("基质扫描被中断。")
                break

            client_rect = get_client_rect(window)

            # 点击坐标（icon_pos_grid 坐标是相对客户区左上角，需要转成屏幕坐标）
            pyautogui.click(client_rect["left"] + rel_x, client_rect["top"] + rel_y)

            # 等待短暂时间以确保界面更新
            time.sleep(0.3)

            screenshot_image = screenshot_window(window, ATTRIBUTE_STATS_ROI)
            result, max_val = recognizer.recognize_roi(screenshot_image)
            logger.success(f"基础属性识别结果: {result} (置信度: {max_val:.3f})")

            screenshot_image = screenshot_window(window, SECONDARY_STATS_ROI)
            result, max_val = recognizer.recognize_roi(screenshot_image)
            logger.success(f"附加属性识别结果: {result} (置信度: {max_val:.3f})")

            screenshot_image = screenshot_window(window, SKILL_STATS_ROI)
            result, max_val = recognizer.recognize_roi(screenshot_image)
            logger.success(f"技能属性识别结果: {result} (置信度: {max_val:.3f})")

            # datetime_str = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%f")
            # save_image(
            #     screenshot_image,
            #     screenshot_dir / f"essence_scan_{datetime_str}.png",
            # )

            time.sleep(0.0)

    def stop(self) -> None:
        logger.info("停止基质扫描线程...")
        self._scanning.clear()


def on_bracket_left():
    """处理 "[" 键按下事件 - 截图"""
    window = get_active_support_window()
    if window is None:
        logger.debug("终末地窗口不在前台，忽略 '[' 键。")
        return
    else:
        logger.info("检测到 '[' 键，开始截图...")

        screenshot_image = screenshot_window(window, ATTRIBUTE_STATS_ROI)
        save_image(
            recognizer.preprocess_roi(screenshot_image),
            screenshot_dir / "attribute_stats_roi.png",
        )
        result, max_val = recognizer.recognize_roi(screenshot_image)
        logger.success(f"基础属性识别结果: {result} (置信度: {max_val:.3f})")

        screenshot_image = screenshot_window(window, SECONDARY_STATS_ROI)
        save_image(
            recognizer.preprocess_roi(screenshot_image),
            screenshot_dir / "secondary_stats_roi.png",
        )
        result, max_val = recognizer.recognize_roi(screenshot_image)
        logger.success(f"附加属性识别结果: {result} (置信度: {max_val:.3f})")

        screenshot_image = screenshot_window(window, SKILL_STATS_ROI)
        save_image(
            recognizer.preprocess_roi(screenshot_image),
            screenshot_dir / "skill_stats_roi.png",
        )
        result, max_val = recognizer.recognize_roi(screenshot_image)
        logger.success(f"技能属性识别结果: {result} (置信度: {max_val:.3f})")


def on_bracket_right():
    """处理 "]" 键按下事件 - 切换自动点击"""
    global click_thread

    if get_active_support_window() is None:
        logger.debug("终末地窗口不在前台，忽略']'键。")
        return
    else:
        if click_thread is None:
            logger.info("检测到 ']' 键，开始依次点击 icon_pos_grid...")
            click_thread = EssenceScanner()
            click_thread.start()
        else:
            logger.info("检测到 ']' 键，停止自动点击")
            click_thread.stop()
            click_thread = None


def on_exit():
    """处理 Alt+Delete 按下事件 - 退出程序"""
    global running, click_thread
    logger.info("检测到 Alt+Delete，退出程序...")
    running = False
    if click_thread is not None:
        click_thread.stop()
        click_thread = None


def main():
    """主函数"""
    global running

    message = """
==================================================
终末地自动化控制脚本已启动

==================================================
功能说明：
  [键：对终末地窗口截图并保存
  ]键：开始/停止持续点击窗口中心
  Alt+Delete：退出程序
==================================================
"""
    logger.success(message)

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
        logger.info("程序被中断，正在退出...")
    finally:
        # 清理
        keyboard.unhook_all()
        logger.info("程序已退出")


if __name__ == "__main__":
    main()
