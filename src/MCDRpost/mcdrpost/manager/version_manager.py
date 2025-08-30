"""版本管理器，根据 Minecraft 版本提供相应的功能实现"""

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item
from mcdrpost.environment import Environment
from mcdrpost.utils.types import Checker
from mcdrpost.version_handler import AbstractVersionHandler


class VersionManager:
    """版本管理器，用于处理不同 Minecraft 版本的特性差异

    根据服务器的 Minecraft 版本，为不同版本提供相应的功能实现，包括物品替换、
    字典转物品对象、物品对象转字符串等功能。

    Attributes:
        environment (Environment): 环境信息对象，包含服务器版本等信息
    """

    _handlers: dict[Checker, type[AbstractVersionHandler]] = {}

    @classmethod
    def register_handler(cls, handler: type[AbstractVersionHandler], checker: Checker) -> None:
        cls._handlers[checker] = handler

    def __init__(self, server: PluginServerInterface) -> None:
        """初始化版本管理器

        Args:
            server (PluginServerInterface): psi 实例
        """
        self._server = server
        self.environment: Environment = Environment(server)
        self._handler: AbstractVersionHandler | None = None

    def refresh(self) -> None:
        """刷新版本相关函数引用

        根据当前服务器版本，更新内部函数引用
        """
        for checker, handler in self._handlers.items():
            # 尝试以environment为参数调用checker
            if checker(self.environment):
                self._handler = handler(self._server)
                break

        else:
            raise RuntimeError(f"No correct handler found for version {self.environment.server_version}")

    # 下面是是依赖版本的函数
    def replace(self, player: str, item: str) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """
        self._handler.replace(player, item)

    def dict2item(self, item: dict) -> Item:
        """将字典转换为物品对象

        Args:
            item (dict): 物品字典

        Returns:
            Item: 物品对象
        """
        return self._handler.dict2item(item)

    def item2str(self, item: Item) -> str:
        """将物品对象转换为物品字符串

        Args:
            item (Item): 物品对象

        Returns:
            str: 物品字符串
        """
        return self._handler.item2str(item)
