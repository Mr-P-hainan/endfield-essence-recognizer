from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

templates_dir = Path("templates")
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

if __name__ == "__main__":
    font = ImageFont.truetype(r"C:\Windows\Fonts\HarmonyOS_SansSC_Regular.ttf", size=22)
    for labels in all_attribute_stats + all_secondary_stats + all_skill_stats:
        image = Image.new("L", (160, 24), color=0)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), labels, font=font, fill=255)
        save_path = templates_dir / f"{labels}.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(save_path)
        print(f"Saved template image: {save_path}")
