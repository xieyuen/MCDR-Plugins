"""MCDRpost API

这是 MCDRpost 暴露出来的一些类，主要是为了用户可以自定义不同 Minecraft 版本的处理器，
防止一些不支持原版命令的服务端导致 MCDRpost 不能正常运行

当然，如果想要使用自定义的命令来得到物品信息也可以，但请不要忘记转换成 Item 类型
"""
from typing import Callable

from mcdrpost.data_structure import Item
from mcdrpost.environment import Environment
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler


def register_handler(handler: type[AbstractVersionHandler], checker: Callable[[Environment], bool]):
    VersionManager.register_handler(handler, checker)


__all__ = [
    "Item",
    "Environment",
    "AbstractVersionHandler",
    "register_handler",
]
