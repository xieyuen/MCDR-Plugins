from typing import TYPE_CHECKING

from mcdreforged import CommandContext, CommandSource, GreedyText, InfoCommandSource, Integer, Literal, \
    PluginServerInterface, RequirementNotMet, Text

from mcdrpost.configuration import CommandPermission, Configuration
from mcdrpost.constants import SIMPLE_HELP_MESSAGE
from mcdrpost.utils import add_requirements
from mcdrpost.utils.command.command_helper import CommandHelper
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class CommandManager:
    """命令管理器"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager: "PostManager" = post_manager
        self._server: PluginServerInterface = post_manager.server
        self.logger = self._server.logger

        self._data_manager = post_manager.data_manager
        self._helper = CommandHelper(self._prefixes, self._data_manager)

        self._prefixes = ["!!po"]

    @property
    def _config(self) -> Configuration:
        return self._post_manager.config

    @property
    def _perm(self) -> CommandPermission:
        return self._config.command_permission

    def register(self) -> None:
        """注册命令树

        在 on_load 中调用
        """
        if self._config.allow_alias:
            self._prefixes = self._config.command_prefixes

        for prefix in self._prefixes:
            self._server.register_help_message(prefix, SIMPLE_HELP_MESSAGE)
            self._server.register_command(
                self.generate_command_node(prefix)
            )

    def receive(self, src: InfoCommandSource, order_id):
        if self._post_manager.receive(src, order_id, 'receive'):
            src.reply(TranslationKeys.receive_success.tr(order_id))

    def cancel(self, src: InfoCommandSource, order_id):
        if self._post_manager.receive(src, order_id, 'cancel'):
            src.reply(TranslationKeys.cancel_success.tr(order_id))

    def add_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.add_player(player):
            src.reply(TranslationKeys.has_player.tr(player))
            return

        src.reply(TranslationKeys.login_success.tr(player))
        self.logger.info(TranslationKeys.login_log.tr(player))

    def remove_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.remove_player(player):
            src.reply(TranslationKeys.cannot_del_player.tr(player))
            return

        src.reply(TranslationKeys.del_player_success.tr(player))
        self.logger.info(TranslationKeys.del_player_log.tr(player))

    # nodes
    def gen_post_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(TranslationKeys.no_input_receiver.tr())).
            then(
                Text('receiver').
                suggests(self._data_manager.get_players).
                runs(lambda src, ctx: self._post_manager.post(src, ctx['receiver'])).
                then(
                    GreedyText('comment').
                    runs(lambda src, ctx: self._post_manager.post(src, ctx['receiver'], ctx['comment']))
                )
            ),
            permission=self._perm.post,
            require_player=True
        )

    def gen_post_list_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).runs(lambda src: self._helper.output_post_list(src)),
            permission=self._perm.post,
            require_player=True
        )

    def gen_receive_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(TranslationKeys.no_input_receive_orderid.tr())).
            then(
                Integer('orderid').
                suggests(
                    lambda src: [
                        str(i) for i in
                        self._data_manager.get_orderid_by_receiver(src.get_info().player)
                    ]
                ).
                runs(lambda src, ctx: self.receive(src, ctx['orderid']))
            ),
            permission=self._perm.receive,
            require_player=True
        )

    def gen_receive_list_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).runs(lambda src: self._helper.output_receive_list(src)),
            permission=self._perm.receive,
            require_player=True
        )

    def gen_cancel_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(TranslationKeys.no_input_cancel_orderid.tr())).
            then(
                Integer('orderid').
                suggests(
                    lambda src: [
                        str(i) for i in
                        self._data_manager.get_orderid_by_sender(src.get_info().player)
                    ]
                ).
                runs(lambda src, ctx: self.cancel(src, ctx['orderid']))
            ),
            permission=self._perm.cancel,
            require_player=True
        )

    def gen_list_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            runs(lambda src: src.reply(TranslationKeys.command_incomplete.tr())).
            then(
                Literal('players').
                requires(lambda src: src.has_permission(self._perm.list_player)).
                runs(lambda src: src.reply(
                    TranslationKeys.list_player_title.tr() + str(self._data_manager.get_players())
                ))
            ).
            then(
                Literal('orders').
                requires(lambda src: src.has_permission(self._perm.list_orders)).
                on_error(RequirementNotMet, lambda src: src.reply(TranslationKeys.no_permission.tr()), handled=True).
                runs(lambda src: self._helper.output_all_orders(src))
            ).
            then(
                add_requirements(
                    Literal('receive').runs(lambda src: self._helper.output_receive_list(src)),
                    permission=self._perm.receive,
                    require_player=True
                )
            ).then(
                add_requirements(
                    Literal('post').runs(lambda src: self._helper.output_post_list(src)),
                    permission=self._perm.post,
                    require_player=True
                )
            )
        )

    def gen_player_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.has_permission(self._perm.player)).
            on_error(RequirementNotMet, lambda src: src.reply(TranslationKeys.no_permission.tr()), handled=True).
            runs(lambda src: src.reply(TranslationKeys.command_incomplete.tr())).
            then(
                Literal('add').
                runs(lambda src: src.reply(TranslationKeys.command_incomplete.tr())).
                then(Text('player_id').runs(self.add_player))
            ).
            then(
                Literal('remove').
                runs(lambda src: src.reply(TranslationKeys.command_incomplete.tr())).
                then(
                    Text('player_id').
                    suggests(self._data_manager.get_players).
                    runs(self.remove_player)
                )
            )
        )

    def gen_reload_node(self, prefix) -> Literal:
        def reload(src: CommandSource):
            self._post_manager.reload()
            src.reply(TranslationKeys.reload_success.tr())

        return (
            Literal(prefix)
            .requires(lambda src: src.has_permission(self._perm.reload))
            .on_error(RequirementNotMet, lambda src: src.reply(TranslationKeys.no_permission.tr()), handled=True)
            .runs(reload)
        )

    def generate_command_node(self, prefix: str) -> Literal:
        """生成指令树"""
        return (
            Literal(prefix).
            requires(lambda src: src.has_permission(self._perm.root)).
            on_error(RequirementNotMet, lambda src: src.reply(TranslationKeys.no_permission.tr()), handled=True).
            runs(lambda src: self._helper.output_help_message(src, prefix)).
            # 下面的一行就是一条命令，多个 then 意味着别名/缩写
            then(self.gen_post_node('p')).then(self.gen_post_node('post')).
            then(self.gen_post_list_node('pl')).then(self.gen_post_list_node('post_list')).
            then(self.gen_receive_node('r')).then(self.gen_receive_node('receive')).
            then(self.gen_receive_list_node('rl')).then(self.gen_receive_list_node('receive_list')).
            then(self.gen_cancel_node('c')).then(self.gen_cancel_node('cancel')).
            then(self.gen_list_node('ls')).then(self.gen_list_node('list')).
            then(self.gen_player_node('player')).
            then(self.gen_reload_node('reload'))
        )
