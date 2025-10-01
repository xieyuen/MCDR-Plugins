from abc import ABC, abstractmethod
from typing import final, override

from mcdreforged import PluginServerInterface, new_thread

import minecraft_data_api as api
from mcdrpost import constants
from mcdrpost.data_structure import Item
from mcdrpost.utils.exception import InvalidItem
from mcdrpost.utils.translation import Tags, tr


class AbstractVersionHandler(ABC):
    """版本处理器

    Attributes:
        server (PluginServerInterface): psi 实例
    """

    @final
    def __init__(self) -> None:
        self.server: PluginServerInterface = PluginServerInterface.psi()

    @classmethod
    @final
    def is_builtin(cls) -> bool:
        """此处理器是否为 MCDRpost 内置的处理器"""
        return cls in BuiltinVersionHandler.__subclasses__()

    @abstractmethod
    def replace(self, player: str, item: Item) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (Item): 物品字符串
        """
        raise NotImplementedError

    @abstractmethod
    def get_offhand_item(self, player: str) -> Item:
        """
        获取玩家副手物品

        Args:
            player (str): 玩家 id
        """
        raise NotImplementedError


class BuiltinVersionHandler(AbstractVersionHandler, ABC):
    """内置版本处理器"""

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

    @override
    def replace(self, player: str, item: Item) -> None:
        """for mc 1.17+"""
        self.server.execute(f'item replace entity {player} weapon.offhand with {self.item2str(item)}')

    @override
    def get_offhand_item(self, player: str) -> Item:
        """获取副手物品--通用实现"""
        if self.server.is_rcon_running():
            offhand_item = api.convert_minecraft_json(
                self.server.rcon_query(f'data get entity {player} {constants.OFFHAND_CODE}')
            )
        else:
            self.server.logger.warning(tr(Tags.rcon.not_running))

            @new_thread('MCDRpost | get offhand item')
            def get():
                return api.get_player_info(player, constants.OFFHAND_CODE)

            # 等待异步执行完成并获取返回值
            offhand_item = get().get_return_value(block=True)

        if not isinstance(offhand_item, dict):
            raise InvalidItem(offhand_item)

        return self.dict2item(offhand_item)
