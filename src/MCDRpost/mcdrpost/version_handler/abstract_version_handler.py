from abc import ABC, abstractmethod
from typing import Any, final, override

from mcdreforged import PluginServerInterface, new_thread

import minecraft_data_api as mc_data_api
from mcdrpost import constants
from mcdrpost.constants import Commands
from mcdrpost.data_structure import Item
from mcdrpost.utils.exception import InvalidItem
from mcdrpost.utils.translation import TranslationKeys
from mcdrpost.version_handler.sound_player.abstract_sound_player import AbstractSoundPlayer
from mcdrpost.version_handler.sound_player.impl import NewSoundPlayer


class AbstractVersionHandler(ABC):
    """版本处理器

    Attributes:
        server (PluginServerInterface): psi 实例
        sound_player (AbstractSoundPlayer): 音效播放器
    """

    @final
    def __init__(self) -> None:
        self.server: PluginServerInterface = PluginServerInterface.psi()
        self.sound_player: AbstractSoundPlayer | None = None

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

    @property
    def play_sound(self) -> AbstractSoundPlayer:
        """播放提示音

        你可以重写这个 property 来更换音效，但请注意刚实例化的 Handler 的 sound_player 属性
        是 None，要判断一下并赋值
        """
        if self.sound_player is None:
            self.sound_player = NewSoundPlayer(self.server)
        return self.sound_player


class BuiltinVersionHandler(AbstractVersionHandler, ABC):
    """内置版本处理器"""

    @staticmethod
    @abstractmethod
    def dict2item(item: dict[str, Any]) -> Item:
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
        self.server.execute(Commands.REPLACE_NEW.format(player, self.item2str(item)))

    @override
    def get_offhand_item(self, player: str) -> Item:
        """获取副手物品--通用实现"""
        if self.server.is_rcon_running():
            offhand_item = mc_data_api.convert_minecraft_json(
                self.server.rcon_query(Commands.GET_ITEM.format(player))
            )
        else:
            self.server.logger.warning(TranslationKeys.rcon.not_running.tr())

            @new_thread('MCDRpost | get offhand item')
            def get():
                return mc_data_api.get_player_info(player, constants.OFFHAND_CODE)

            # 等待异步执行完成并获取返回值
            offhand_item = get().get_return_value(block=True)

        if not isinstance(offhand_item, dict):
            raise InvalidItem(offhand_item)  # TODO: 更换方式

        return self.dict2item(offhand_item)

    def __repr__(self):
        return f"<MCDRpostBuiltinVersionHandler {self.__class__.__name__} handler at {id(self)}>"
