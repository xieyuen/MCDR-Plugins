import time
from typing import TypeVar

from mcdreforged import AbstractNode, CommandSource, RequirementNotMet

from mcdrpost.utils.translation import Tags, tr


def get_formatted_time() -> str:
    """获取当前时间的格式化的字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


__Node = TypeVar("__Node", bound=AbstractNode)


def add_requirements(node: __Node, permission: int, require_player: bool = False) -> __Node:
    def require_callback(src: CommandSource) -> bool:
        if require_player and not src.is_player:
            return False
        if not src.has_permission(permission):
            return False
        return True

    def on_error(src: CommandSource):
        if require_player and not src.is_player:
            src.reply(tr(Tags.only_for_player))
            return
        src.reply(tr(Tags.no_permission))

    node.requires(require_callback).on_error(
        RequirementNotMet, on_error, handled=True
    )

    return node


__all__ = ['get_formatted_time', 'add_requirements']
