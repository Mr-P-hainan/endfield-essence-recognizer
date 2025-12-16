from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Record

# default_format: str = (
#     '<dim>File <cyan>"{file.path}"</>, line <cyan>{line}</>, in <cyan>{function}</></>\n'
#     "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> "
#     "[<level>{level}</>] "
#     "<level><normal>{message}</></>"
# )

default_format: str = (
    '<dim>File <cyan>"{file.path}"</>, line <cyan>{line}</>, in <cyan>{function}</></>\n'
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> "
    '<cyan>"{file.path}"</>, line <cyan>{line}</>, in <cyan>{function}</>'
    "[<level>{level}</>] "
    "<level><normal>{message}</></>"
)


def default_filter(record: Record):
    """默认的日志过滤器，根据 `config.log_level` 配置改变日志等级。"""
    log_level = record["extra"].get("arknights_game_model_log_level", "INFO")
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    return record["level"].no >= levelno


logger.remove()
logger.add(
    sys.stderr,
    level=0,
    format=default_format,
    filter=default_filter,
    diagnose=True,
)
