"""版本管理器，根据 Minecraft 版本提供相应的功能实现"""
from typing import Callable, final

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item
from mcdrpost.environment import Environment
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler

Checker = Callable[[Environment], bool]


class VersionManager:
    """版本管理器，用于处理不同 Minecraft 版本的特性差异

    根据服务器的 Minecraft 版本，为不同版本提供相应的功能实现，包括物品替换、
    字典转物品对象、物品对象转字符串等功能。

    Attributes:
        environment (Environment): 环境信息对象，包含服务器版本等信息
    """

    _handlers: list[tuple[Checker, AbstractVersionHandler]] = []
    _builtin_handlers: list[tuple[Checker, AbstractVersionHandler]] = []

    @classmethod
    @final
    def register_handler(cls, handler: type[AbstractVersionHandler], checker: Checker) -> None:
        """注册 Handler

        Args:
            handler (type[AbstractVersionHandler]): 要注册的 handler 类
            checker (Callable[[Environment], bool]): 判断 handler 是否应该使用
        """
        if handler.is_builtin():
            cls._builtin_handlers.append((checker, handler()))
        else:
            cls._handlers.append((checker, handler()))

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

        .. note::
            插件会优先使用外部注册的 Handler

        Raises:
            RuntimeError: 如果没有找到合适的 VersionHandler 的话
        """
        for checker, handler in self._handlers:
            if checker(self.environment):
                self._handler = handler
                return

        for checker, handler in self._builtin_handlers:
            if checker(self.environment):
                self._handler = handler
                return

        raise RuntimeError(f"No correct handler found for version {self.environment.server_version}")

    # 下面是是依赖版本的函数
    def replace(self, player: str, item: Item) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """
        if self._handler is None:
            raise RuntimeError("version handler is not initialized")
        self._handler.replace(player, item)

    def get_offhand_item(self, player: str) -> Item:
        """获取玩家副手物品

        Args:
            player (str): 玩家名
        """
        if self._handler is None:
            raise RuntimeError("version handler is not initialized")
        return self._handler.get_offhand_item(player)
