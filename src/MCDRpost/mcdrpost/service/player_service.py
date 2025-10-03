"""
玩家管理服务
"""
from typing import TYPE_CHECKING

from mcdreforged import CommandSource, CommandContext

from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class PlayerService:
    """玩家管理服务"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager = post_manager
        self._data_manager = post_manager.data_manager
        self._server = post_manager.server
        self._logger = post_manager.server.logger

    def add_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.add_player(player):
            src.reply(TranslationKeys.has_player.tr(player))
            return

        src.reply(TranslationKeys.login_success.tr(player))
        self._logger.info(TranslationKeys.login_log.tr(player))

    def remove_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.remove_player(player):
            src.reply(TranslationKeys.cannot_del_player.tr(player))
            return

        src.reply(TranslationKeys.del_player_success.tr(player))
        self._logger.info(TranslationKeys.del_player_log.tr(player))