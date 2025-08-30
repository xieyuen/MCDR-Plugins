"""版本管理器，根据 Minecraft 版本提供相应的功能实现"""

from typing import TYPE_CHECKING

from mcdrpost.data_structure import Item
from mcdrpost.environment import Environment
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler
from mcdrpost.version_handler.before_1_17 import Before17Handler
from mcdrpost.version_handler.since_1_17 import Since17Handler
from mcdrpost.version_handler.since_1_20_5 import Since20Handler

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class VersionManager:
    """版本管理器，用于处理不同Minecraft版本的特性差异

    根据服务器的 Minecraft 版本，为不同版本提供相应的功能实现，包括物品替换、
    字典转物品对象、物品对象转字符串等功能。

    Attributes:
        environment (Environment): 环境信息对象，包含服务器版本等信息
        handler (AbstractVersionHandler): MC 版本处理器
    """

    def __init__(self, pm: "PostManager"):
        """初始化版本管理器

        Args:
            pm (PostManager): PostManager 实例
        """
        self._server = pm.server
        self.environment: Environment = Environment(pm.server)
        self.handler: AbstractVersionHandler | None = None

    def refresh(self) -> None:
        """刷新版本相关函数引用

        根据当前服务器版本，更新内部函数引用
        """
        if self.environment.server_version < "1.17":
            self.handler = Before17Handler(self._server)
        elif self.environment.server_version < "1.20.5":
            self.handler = Since17Handler(self._server)
        else:
            self.handler = Since20Handler(self._server)

    # 下面是是依赖版本的函数

    def replace(self, player: str, item: str) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """
        self.handler.replace(player, item)

    def dict2item(self, item: dict) -> Item:
        """将字典转换为物品对象

        Args:
            item (dict): 物品字典

        Returns:
            Item: 物品对象
        """
        return self.handler.dict2item(item)

    def item2str(self, item: Item) -> str:
        """将物品对象转换为物品字符串

        Args:
            item (Item): 物品对象

        Returns:
            str: 物品字符串
        """
        return self.handler.item2str(item)
