from abc import ABC, abstractmethod
from typing import final

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


class AbstractVersionHandler(ABC):
    """版本处理器

    Attributes:
        server (PluginServerInterface): psi 实例
    """

    @final
    def __init__(self) -> None:
        self.server: PluginServerInterface = PluginServerInterface.psi()

    @final
    @property
    def is_builtin(self) -> bool:
        """此处理器是否为 MCDRpost 内置的处理器"""
        return isinstance(self, BuiltinVersionHandler)

    @abstractmethod
    def replace(self, player: str, item: str) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def dict2item(item: dict) -> Item:
        """将物品字典转换为物品对象

        Args:
            item (dict): 物品字典

        Returns:
            Item: 物品对象
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def item2str(item: Item) -> str:
        """将物品对象转换为物品字符串

        Args:
            item (Item): 物品对象

        Returns:
            str: 物品字符串
        """
        raise NotImplementedError


class BuiltinVersionHandler(AbstractVersionHandler, ABC):
    """内置版本处理器"""
