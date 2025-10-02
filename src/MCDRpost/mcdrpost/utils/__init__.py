import time
from typing import TypeVar

from mcdreforged import AbstractNode, CommandSource, RequirementNotMet

from mcdrpost.utils.translation import TranslationKeys


def get_formatted_time() -> str:
    """获取当前时间的格式化的字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


# 其实想用 3.12 的泛型语法的
# 但是还是要保证兼容性
# TODO: 此注解应该在 MCDR 产生放弃 3.10 版本的更新时替换成 3.12 的新泛型语法
__NodeType = TypeVar("__NodeType", bound=AbstractNode)


def add_requirements(node: __NodeType, permission: int, require_player: bool = False) -> __NodeType:
    def require_callback(src: CommandSource) -> bool:
        if require_player and not src.is_player:
            return False
        if not src.has_permission(permission):
            return False
        return True

    def on_require_not_met(src: CommandSource):
        if require_player and not src.is_player:
            src.reply(TranslationKeys.only_for_player.tr())
            return
        src.reply(TranslationKeys.no_permission.tr())

    node.requires(require_callback).on_error(
        RequirementNotMet, on_require_not_met, handled=True
    )

    return node


__all__ = ['get_formatted_time', 'add_requirements']
