"""版本管理器，根据 Minecraft 版本提供相应的功能实现"""

from typing import TYPE_CHECKING

from mcdrpost.data_structure import Item
from mcdrpost.environment import Environment
from mcdrpost.utils.types import Dict2ItemFunction, Item2StrFunction, ReplaceFunction
from mcdrpost.version import after1_20_5, before1_17, from_1_17_to_1_20_5

if TYPE_CHECKING:
    from new.manager.post_manager import PostManager  # noqa


class VersionManager:
    """版本管理器，用于处理不同Minecraft版本的特性差异

    根据服务器的 Minecraft 版本，为不同版本提供相应的功能实现，包括物品替换、
    字典转物品对象、物品对象转字符串等功能。

    Attributes:
        environment (Environment): 环境信息对象，包含服务器版本等信息
    """

    def __init__(self, pm: "PostManager"):
        """初始化版本管理器

        Args:
            pm (PostManager): PostManager 实例
        """
        self._server = pm.server
        self.environment: Environment = Environment(pm.server)
        self._replace: ReplaceFunction | None = None
        self._dict2item: Dict2ItemFunction | None = None
        self._item2str: Item2StrFunction | None = None

    def refresh(self) -> None:
        """刷新版本相关函数引用

        根据当前服务器版本，更新内部函数引用
        """
        if self.environment.server_version < "1.17":
            self._replace = before1_17.replace
            self._dict2item = before1_17.dict2item
            self._item2str = before1_17.item2str
        elif self.environment.server_version < "1.20.5":
            self._replace = from_1_17_to_1_20_5.replace
            self._dict2item = from_1_17_to_1_20_5.dict2item
            self._item2str = from_1_17_to_1_20_5.item2str
        else:
            self._replace = after1_20_5.replace
            self._dict2item = after1_20_5.dict2item
            self._item2str = after1_20_5.item2str

    # 下面是是依赖版本的函数

    def replace(self, player: str, item: Item) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """
        self._replace(self._server, player, self._item2str(item))  # noqa

    def dict2item(self, item: dict) -> Item:
        """将字典转换为物品对象

        Args:
            item (dict): 物品字典

        Returns:
            Item: 物品对象
        """
        return self._dict2item(item)  # noqa
