import time
from typing import TypeVar

from mcdreforged import AbstractNode, CommandSource, RequirementNotMet

from mcdrpost.utils.translation import TranslationKeys


def get_formatted_time() -> str:
    """获取当前时间的格式化的字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())





__all__ = ['get_formatted_time']
