import sys
from pathlib import Path

if getattr(sys, "frozen", False) and (_MEIPASS := getattr(sys, "_MEIPASS", None)):
    ROOT_DIR = Path(_MEIPASS).parent.resolve()

else:
    ROOT_DIR = Path().resolve()
