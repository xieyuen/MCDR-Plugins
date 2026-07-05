from abc import ABC, abstractmethod

from mcdreforged import ServerInterface

from mcdrpost import constants
from mcdrpost.data_structure import Item
from mcdrpost.mcva.environment import Environment
from mcdrpost.utils.translation import TranslationKeys


class AbstractMCVersionAdaptor(ABC):
    """Minecraft 不同版本的兼容性适配器抽象基类"""

    server: ServerInterface = ServerInterface.si()
    """MCDR 服务器接口"""

    @classmethod
    def is_builtin(cls) -> bool:
        """是否为内置 Adaptor

        当且仅当直接继承自 BuiltinAdaptor 的才是内置的
        """
        return cls in BuiltinAdaptor.__subclasses__()

    @abstractmethod
    def get_offhand_item(self, player: str) -> Item:
        """获取玩家副手物品

        Args:
            player (str): 玩家名

        Returns:
            Item: 副手物品的信息
        """
        raise NotImplementedError

    @abstractmethod
    def get_replace_command(self, player: str, item: Item) -> str:
        """获取 ``replaceitem``/``item replace`` 命令字符串

        可以用 constant.Commands 内的模板字符串进行格式化

        Args:
            player (str): 玩家名称
            item (Item): 物品信息, 包括 ID、数量和 组件信息/tag 信息

        Returns:
            str: 适用于当前 Minecraft 版本的命令字符串
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_usable(env: Environment) -> bool:
        """判断此适配器是否适用于当前环境"""
        raise NotImplementedError

    def __repr__(self):
        return f"MCDRpostAdaptor<{self.__class__.__name__} at {hex(id(self))}>"


class BuiltinAdaptor(AbstractMCVersionAdaptor, ABC):
    def get_offhand_item(self, player: str) -> Item:
        import minecraft_data_api as mc_data_api

        if self.server.is_rcon_running():
            offhand_item = mc_data_api.convert_minecraft_json(
                self.server.rcon_query(Commands.GET_ITEM.format(player)),  # type: ignore
            )
        else:
            self.server.logger.warning(TranslationKeys.rcon_not_running.rtr())
            offhand_item = mc_data_api.get_player_info(player, constants.OFFHAND_CODE)

        return self.dict2item(offhand_item)

    @staticmethod
    @abstractmethod
    def dict2item(data: dict) -> Item:
        raise NotImplementedError
