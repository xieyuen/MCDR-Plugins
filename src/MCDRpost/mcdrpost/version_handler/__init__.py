import importlib
from abc import ABC, abstractmethod
from pathlib import Path

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


class AbstractVersionHandler(ABC):
    """版本处理器

    Attributes:
        server (PluginServerInterface): psi 实例
    """

    def __init__(self, server: PluginServerInterface):
        self.server = server

    @abstractmethod
    def replace(self, player: str, item: str) -> None:
        """替换玩家副手物品

        Args:
            player (str): 玩家名
            item (str): 物品字符串
        """

    @staticmethod
    @abstractmethod
    def dict2item(item: dict) -> Item:
        """将物品字典转换为物品对象

        Args:
            item (dict): 物品字典

        Returns:
            Item: 物品对象
        """

    @staticmethod
    @abstractmethod
    def item2str(item: Item) -> str:
        """将物品对象转换为物品字符串

        Args:
            item (Item): 物品对象

        Returns:
            str: 物品字符串
        """


def register_all_handlers():
    """自动导入version_handler目录下所有模块（除了__init__.py和abstract_version_handler.py）

    通过动态导入所有版本处理器模块，触发它们的自动注册机制
    """
    # 获取当前模块所在目录
    current_dir = Path(__file__).parent

    # 遍历目录中的所有.py文件
    for file_path in current_dir.glob("*.py"):
        module_name = file_path.stem

        # 跳过__init__.py和abstract_version_handler.py
        if module_name in ("__init__", "abstract_version_handler"):
            continue

        # 动态导入模块，触发其中的注册代码
        importlib.import_module(f"mcdrpost.version_handler.{module_name}")
