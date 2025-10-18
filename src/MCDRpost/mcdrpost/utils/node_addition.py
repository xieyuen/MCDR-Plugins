from mcdreforged import AbstractNode, CommandSource, RequirementNotMet

from mcdrpost.utils.translation import TranslationKeys


def add_requirements[NodeType: AbstractNode](
        node: NodeType,
        permission: int,
        require_player: bool = False
) -> NodeType:
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
