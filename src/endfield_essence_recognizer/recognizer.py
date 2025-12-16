import itertools
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from cv2.typing import MatLike

from endfield_essence_recognizer.image import (
    linear_operation,
    load_image,
    to_gray_image,
)
from endfield_essence_recognizer.log import logger

# 识别ROI区域（客户区像素坐标）
# 该区域显示基质的属性文本，如"智识提升"等
BONUS_ROI = (1508, 359, 1680, 390)  # (x1, y1, x2, y2)

# 识别标签列表（所有可能的属性文本）
BONUS_LABELS = ["智识提升", "敏捷提升", "力量提升", "意志提升", "全能力提升"]
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"  # 模板图片目录

# 识别阈值（默认值，可在 Recognizer 中覆盖）
HIGH_THRESH = 0.75  # 高置信度阈值：超过此值直接判定
LOW_THRESH = 0.50  # 低置信度阈值：低于此值判定为未知


class Recognizer:
    """封装模板加载与ROI识别逻辑，便于复用与测试。"""

    def __init__(
        self,
        labels: list[str],
        templates_dir: Path,
        high_thresh: float = HIGH_THRESH,
        low_thresh: float = LOW_THRESH,
    ) -> None:
        self.labels: list[str] = labels
        self.templates_dir: Path = templates_dir
        self.high_thresh: float = high_thresh
        self.low_thresh: float = low_thresh
        self._template_cache: defaultdict[str, list[np.ndarray]] = defaultdict(list)
        self._exts: list[str] = [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tiff",
            ".webp",
            ".gif",
            ".tif",
        ]

        self.load_templates()

    def load_templates(self) -> None:
        if not self.templates_dir.exists():
            logger.error(f"模板目录未找到: {self.templates_dir}")
            return

        for label in self.labels:
            for path in itertools.chain(
                self.templates_dir.glob(label + "*"),
                (self.templates_dir / label).glob("**/*"),
            ):
                if path.suffix.lower() in self._exts and path.is_file():
                    try:
                        image = load_image(path, cv2.IMREAD_GRAYSCALE)
                        image = self.preprocess_template(image)
                        self._template_cache[label].append(image)
                    except Exception as e:
                        logger.error(f"加载模板图像失败 {path}: {e}")
            if not self._template_cache[label]:
                logger.warning(f"在 {self.templates_dir} 中未找到标签 '{label}' 的模板")

    def preprocess_roi(self, roi_image: MatLike) -> MatLike:
        """对 ROI 图像进行预处理，提升识别效果。"""
        gray = to_gray_image(roi_image)
        enhanced = linear_operation(gray, 100, 255)
        return enhanced

    def preprocess_template(self, template_image: MatLike) -> MatLike:
        """对模板图像进行预处理，提升识别效果。"""
        return linear_operation(template_image, 128, 255)

    def recognize_roi(self, roi_image: MatLike) -> tuple[str | None, float]:
        """
        识别 ROI 图像中的短语，返回 (标签, 置信度)。

        Args:
            roi_img: ROI 区域的图像（OpenCV 格式）

        Returns:
            (标签, 置信度) 元组。如果无法识别，返回 (None, best_score)。
        """

        image_height, image_width = roi_image.shape[:2]
        gray = to_gray_image(roi_image)

        best_label = None
        best_score = -float("inf")
        for label, templates in self._template_cache.items():
            for template in templates:
                template_height, template_width = template.shape[:2]
                if image_height < template_height or image_width < template_width:
                    logger.warning(
                        f"标签 '{label}' 的 ROI 图像小于模板: "
                        f"ROI 尺寸={gray.shape[::-1]}, 模板尺寸={template.shape[::-1]}"
                    )
                    continue
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                _minVal, maxVal, _minLoc, _maxLoc = cv2.minMaxLoc(result)
                logger.debug(f"模板匹配: 标签={label} 最大值={maxVal:.3f}")
                if maxVal > best_score:
                    best_score = maxVal
                    best_label = label

        if best_score >= self.high_thresh:
            return best_label, float(best_score)
        elif best_score >= self.low_thresh:
            logger.warning(f"匹配置信水平较低: 标签={best_label} 分数={best_score:.3f}")
            return best_label, float(best_score)
        else:
            logger.warning(f"匹配置信水平很低: 标签={best_label} 分数={best_score:.3f}")
            return None, float(best_score)
