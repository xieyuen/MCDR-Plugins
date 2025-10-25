import time
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from mcdrpost.utils.translation import TranslationKeys


def get_formatted_time() -> str:
    """获取当前时间的格式化的字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# TODO: to 3.12 generic grammar (see dev/MCDRpost-3.12)
ComparableType = TypeVar("ComparableType")


class TotalOrdering(Generic[ComparableType], ABC):
    @abstractmethod
    def __eq__(self, other) -> bool:  # self == other
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other: ComparableType) -> bool:  # self < other
        raise NotImplementedError

    def __le__(self, other: ComparableType) -> bool:  # self <= other
        return self < other or self == other

    def __gt__(self, other: ComparableType) -> bool:  # self > other
        return not (self <= other)

    def __ge__(self, other: ComparableType) -> bool:  # self >= other
        return not (self < other)


__all__ = ['get_formatted_time', "TotalOrdering"]
