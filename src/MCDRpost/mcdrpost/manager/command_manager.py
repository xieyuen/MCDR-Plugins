from typing import TYPE_CHECKING

from mcdreforged import CommandContext, CommandSource, GreedyText, InfoCommandSource, Integer, Literal, \
    PluginServerInterface, RAction, \
    RColor, RText, RTextList, RequirementNotMet, Text

from mcdrpost.configuration import CommandPermission, Configuration
from mcdrpost.constants import END_LINE, SIMPLE_HELP_MESSAGE
from mcdrpost.utils import add_requirements
from mcdrpost.utils.translation import Tags, tr

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class CommandManager:
    """命令管理器"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager: "PostManager" = post_manager
        self._server: PluginServerInterface = post_manager.server
        self.logger = self._server.logger

        self._data_manager = post_manager.data_manager

        self._prefixes = ["!!po"]

    @property
    def _config(self) -> Configuration:
        return self._post_manager.configuration

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

    # helper methods
    def output_help_message(self, source: CommandSource, prefix: str) -> None:
        """辅助函数：打印帮助信息"""
        msgs_on_helper = RText('')
        msgs_on_admin = RText('')
        if source.has_permission(2):
            # helper以上权限的添加信息
            msgs_on_helper = RTextList(
                RText(prefix + ' list orders', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list orders")
                .h(tr('hover')),

                RText(tr(Tags.help.hint_ls_orders) + END_LINE),
            )
        if source.has_permission(3):
            # admin以上权限的添加信息
            msgs_on_admin = RTextList(
                RText(prefix + tr(Tags.help.player_add), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player add ")
                .h(tr('hover')), RText(f'{tr("help.hint_player_add")}\n'),

                RText(prefix + tr(Tags.help.player_remove), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player remove ")
                .h(tr('hover')), RText(f'{tr("help.hint_player_remove")}\n'),
            )

        source.reply(
            RTextList(
                RText('--------- §3MCDRpost §r---------\n'),
                RText(tr(Tags.desc) + END_LINE),
                RText(tr(Tags.help.title) + END_LINE),
                RText(prefix, RColor.gray).c(RAction.suggest_command, prefix).h(tr('hover')),
                RText(f' | {tr(Tags.help.hint_help)}\n'),
                RText(prefix + tr(Tags.help.p), RColor.gray).c(RAction.suggest_command, f"{prefix} post").h(
                    tr(Tags.hover)),
                RText(f'{tr(Tags.help.hint_p)}\n'),
                RText(prefix + ' rl', RColor.gray).c(RAction.suggest_command, f"{prefix} receive_list").h(tr('hover')),
                RText(f'{tr(Tags.help.hint_rl)}\n'),
                RText(prefix + tr('help.r'), RColor.gray).c(RAction.suggest_command, f"{prefix} receive").h(
                    tr('hover')),
                RText(f'{tr(Tags.help.hint_r)}\n'),
                RText(prefix + ' pl', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} post_list").h(tr('hover')),
                RText(f'{tr(Tags.help.hint_pl)}\n'),
                RText(prefix + tr(Tags.help.c), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} cancel").h(tr('hover')),
                RText(f'{tr(Tags.help.hint_c)}\n'),
                RText(prefix + ' ls players', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list players").h(tr('hover')),
                RText(f'{tr(Tags.help.hint_ls_players)}\n'),
                msgs_on_helper,
                msgs_on_admin,
                RText("§a『别名 Alias』§r\n"),
                RText("    list -> ls 或 l\n", RColor.gray),
                RText("    receive -> r\n", RColor.gray),
                RText("    post -> p\n", RColor.gray),
                RText("    cancel -> c\n", RColor.gray),
                RText(f'根指令: {", ".join(self._prefixes)}\n'),
                RText('-----------------------'),
            )
        )

    def output_post_list(self, src: InfoCommandSource) -> None:
        """辅助函数：输出玩家发送的订单列表"""
        post_list = self._data_manager.get_orders_by_sender(
            src.get_info().player
        )

        if not post_list:
            src.reply(tr(Tags.no_post_orders))
            return

        msg = ""

        for order in post_list:
            msg += f"{order.id}  | {order.receiver}  | {order.time}  | {order.comment}\n"

        src.reply(
            '===========================================\n'
            '{0}\n'
            '{1}'
            '-------------------------------------------\n'
            '{2}'
            '===========================================\n'
            .format(tr(Tags.list_post_orders_title), msg, tr(Tags.hint_cancel))
        )

    def output_receive_list(self, src: InfoCommandSource) -> None:
        """辅助函数：输出玩家待接收的邮件列表"""
        receive_list = self._data_manager.get_orders_by_receiver(
            src.get_info().player
        )

        if not receive_list:
            src.reply(tr(Tags.no_receive_orders))
            return

        msg = ""

        for order in receive_list:
            msg += f"{order.id}  | {order.sender}  | {order.time}  | {order.comment}\n"

        src.reply(
            '===========================================\n'
            '{0}\n'
            '{1}\n'
            '-------------------------------------------\n'
            '{2}'
            '===========================================\n'
            .format(tr(Tags.list_receive_orders_title), msg, tr(Tags.hint_order_receive))
        )

    def output_all_orders(self, src: InfoCommandSource) -> None:
        """辅助函数：输出所有订单列表"""
        all_orders = self._data_manager.get_orders()

        if not all_orders:
            src.reply(tr(Tags.no_orders))
            return

        msg = ""

        for order in all_orders:
            msg += f"{order.id}  | {order.sender}  | {order.receiver}  | {order.time}  | {order.comment}\n"

        src.reply(
            '===========================================\n'
            '{0}\n'
            '{1}\n'
            '===========================================\n'
            .format(tr(Tags.list_orders_title), msg)
        )

    def receive(self, src: InfoCommandSource, order_id):
        if self._post_manager.receive(src, order_id, 'receive'):
            src.reply(tr(Tags.receive_success, order_id))

    def cancel(self, src: InfoCommandSource, order_id):
        if self._post_manager.receive(src, order_id, 'cancel'):
            src.reply(tr(Tags.cancel_success, order_id))

    def add_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.add_player(player):
            src.reply(tr(Tags.has_player, player))
            return

        src.reply(tr(Tags.login_success, player))
        self.logger.info(tr(Tags.login_log, player))

    def remove_player(self, src: CommandSource, ctx: CommandContext):
        player = ctx['player_id']
        if not self._data_manager.remove_player(player):
            src.reply(tr(Tags.cannot_del_player, player))
            return

        src.reply(tr(Tags.del_player_success, player))
        self.logger.info(tr(Tags.del_player_log, player))

    # nodes
    def gen_post_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(tr(Tags.no_input_receiver))).
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
            Literal(node_name).runs(lambda src: self.output_post_list(src)),
            permission=self._perm.post,
            require_player=True
        )

    def gen_receive_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(tr(Tags.no_input_receive_orderid))).
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
            Literal(node_name).runs(lambda src: self.output_receive_list(src)),
            permission=self._perm.receive,
            require_player=True
        )

    def gen_cancel_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).
            runs(lambda src: src.reply(tr(Tags.no_input_cancel_orderid))).
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
            runs(lambda src: src.reply(tr(Tags.command_incomplete))).
            then(
                Literal('players').
                requires(lambda src: src.has_permission(self._perm.list_player)).
                runs(lambda src: src.reply(
                    tr(Tags.list_player_title) + str(self._data_manager.get_players())
                ))
            ).
            then(
                Literal('orders').
                requires(lambda src: src.has_permission(self._perm.list_orders)).
                on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
                runs(lambda src: self.output_all_orders(src))
            ).
            then(
                add_requirements(
                    Literal('receive').runs(lambda src: self.output_receive_list(src)),
                    permission=self._perm.receive,
                    require_player=True
                )
            ).then(
                add_requirements(
                    Literal('post').runs(lambda src: self.output_post_list(src)),
                    permission=self._perm.post,
                    require_player=True
                )
            )
        )

    def gen_player_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.has_permission(self._perm.player)).
            on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
            runs(lambda src: src.reply(tr(Tags.command_incomplete))).
            then(
                Literal('add').
                runs(lambda src: src.reply(tr(Tags.command_incomplete))).
                then(Text('player_id').runs(self.add_player))
            ).
            then(
                Literal('remove').
                runs(lambda src: src.reply(tr(Tags.command_incomplete))).
                then(
                    Text('player_id').
                    suggests(self._data_manager.get_players).
                    runs(self.remove_player)
                )
            )
        )

    def gen_reload_node(self, prefix) -> Literal:
        return (
            Literal(prefix)
            .requires(lambda src: src.has_permission(self._perm.reload))
            .on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True)
            .runs(lambda src: (self._post_manager.reload(), src.reply(tr(Tags.reload_success))))
        )

    def generate_command_node(self, prefix: str) -> Literal:
        """生成指令树"""
        return (
            Literal(prefix).
            requires(lambda src: src.has_permission(self._perm.root)).
            on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
            runs(lambda src: self.output_help_message(src, prefix)).
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
