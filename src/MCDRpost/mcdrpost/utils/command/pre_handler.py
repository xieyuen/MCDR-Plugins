from typing import TYPE_CHECKING, cast

from mcdreforged import CommandContext, CommandSource, PlayerCommandSource

from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager
    from mcdrpost.manager.data_manager import DataManager
    from mcdrpost.coordinator import MCDRpostCoordinator


class CommandPreHandler:
    def __init__(self, coo: "MCDRpostCoordinator"):
        self.logger = coo.logger
        self._post_manager: "PostManager" = coo.post_manager
        self._data_manager: "DataManager" = coo.data_manager

    def post(self, src: CommandSource, ctx: CommandContext):
        self._post_manager.post(
            cast(PlayerCommandSource, src), ctx["receiver"], ctx.get("comment")
        )

    def receive(self, src: CommandSource, ctx: CommandContext):
        order_id = ctx["orderid"]
        if self._post_manager.receive(
                cast(PlayerCommandSource, src), order_id, "receive"
        ):
            src.reply(TranslationKeys.receive_success.tr(order_id))

    def cancel(self, src: CommandSource, ctx: CommandContext):
        order_id = ctx["orderid"]
        if self._post_manager.receive(
                cast(PlayerCommandSource, src), order_id, "cancel"
        ):
            src.reply(TranslationKeys.cancel_success.tr(order_id))

    def add_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx["player_id"]
        if not self._data_manager.add_player(player):
            src.reply(TranslationKeys.player_fail_already_registered.rtr(player))
            return

        src.reply(TranslationKeys.player_registered.rtr(player))
        self.logger.info(TranslationKeys.data_auto_register.rtr(player))

    def remove_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx["player_id"]
        if not self._data_manager.remove_player(player):
            src.reply(TranslationKeys.player_fail_unable_del.rtr(player))
            return

        src.reply(TranslationKeys.player_removed.rtr(player))
        self.logger.info(TranslationKeys.player_removed.rtr(player))
