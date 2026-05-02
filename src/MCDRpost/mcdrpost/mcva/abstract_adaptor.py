from abc import ABC, abstractmethod

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item
from mcdrpost.mcva.environment import Environment


class AbstractMCVersionAdaptor(ABC):
    """Minecraft 不同版本的兼容性适配器抽象基类

    Attributes:
        server: MCDR 服务器接口
    """

    def __init__(self, server: PluginServerInterface):
        self.server = server

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
    def get_replace_command(self, item: Item) -> str:
        """获取 ``replaceitem``/``item replace`` 命令字符串

        可以用 constant.Commands 内的模板字符串进行格式化

        Args:
            item (Item): 物品信息, 包括 ID、数量和 组件信息/tag 信息

        Returns:
            str: 适用于当前 Minecraft 版本的命令字符串
        """
        raise NotImplementedError

    @abstractmethod
    def is_usable(self, env: Environment) -> bool:
        raise NotImplementedError
