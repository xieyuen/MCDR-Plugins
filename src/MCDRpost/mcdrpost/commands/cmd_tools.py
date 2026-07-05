from typing import Callable, TYPE_CHECKING

from mcdreforged import CommandContext, CommandSource, RTextMCDRTranslation

from mcdrpost.core.services.post_service import ReceivingStatsCode
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


def require_perm(perm: int) -> Callable[[CommandSource], bool]:
    return lambda src: src.has_permission(perm)


def require_player(src: CommandSource) -> bool:
    return src.is_player


def cannot_used_by_console(src: CommandSource):
    src.reply(TranslationKeys.error_player_only.rtr())


def reply(msg: str | RTextMCDRTranslation) -> Callable[[CommandSource], None]:
    return lambda src: src.reply(msg)


def reply_incomplete_cmd(src: CommandSource) -> None:
    src.reply(TranslationKeys.error_incomplete_general.rtr())


def post(mcdrpost: "MCDRpostMain") -> Callable[[CommandSource, CommandContext], None]:
    def _post(src: CommandSource, ctx: CommandContext):
        assert src.is_player
        mcdrpost.post_service.send(
            src.player,  # type: ignore
            ctx["receiver"], ctx.get("comments"),
        )

    return _post


def receive(mcdrpost: "MCDRpostMain") -> Callable[[CommandSource, CommandContext], None]:
    def _receive(src: CommandSource, ctx: CommandContext):
        assert src.is_player
        order_id = ctx["order_id"]
        return_code = mcdrpost.post_service.receive(
            src.player,  # type:ignore
            order_id,
        )
        if return_code == ReceivingStatsCode.success:
            src.reply(TranslationKeys.receive_success.rtr(order_id))
        elif return_code == ReceivingStatsCode.order_unexisted:
            src.reply(TranslationKeys.receive_fail_undefined_id)
        elif return_code == ReceivingStatsCode.order_belongs_to_other:
            src.reply(TranslationKeys.receive_fail_no_right)

    return _receive
