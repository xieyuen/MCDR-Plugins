from typing import Literal as LiteralType, TYPE_CHECKING

from mcdreforged.api.command import GreedyText, Integer, Literal, RequirementNotMet, Text
from mcdreforged.api.rtext import RAction, RColor, RText, RTextList
from mcdreforged.api.types import CommandSource, InfoCommandSource, PluginServerInterface

from mcdrpost.config.configuration import CommandPermission
from mcdrpost.constants import END_LINE
from mcdrpost.utils import tr
from mcdrpost.utils.translation_tags import Tags

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager  # noqa


class CommandManager:
    """命令管理器"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager: "PostManager" = post_manager
        self._server: PluginServerInterface = post_manager.server
        self._prefixes: list[str] = post_manager.config_manager.configuration.command_prefixes
        self._perm: CommandPermission = post_manager.config_manager.configuration.command_permission

    def register(self) -> None:
        """注册命令树

        在 on_load 中调用
        """
        for prefix in self._prefixes:
            self._server.register_help_message(prefix, {
                "en_us": "post/teleport weapon hands items",
                "zh_cn": "传送/收寄副手物品",
            })
            self._server.register_command(
                self.generate_command_node(prefix)
            )

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
        post_list = self._post_manager.order_manager.get_orders_by_sender(
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
        receive_list = self._post_manager.order_manager.get_orders_by_receiver(
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
        all_orders = self._post_manager.order_manager.get_orders()

        if not all_orders:
            src.reply(tr(Tags.no_orders))

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

    def gen_post_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.is_player and src.has_permission(self._perm.post)).
            on_error(RequirementNotMet, lambda src: src.reply(
                tr(Tags.no_permission if src.is_player else Tags.only_for_player)
            ), handled=True).
            runs(lambda src: src.reply(tr(Tags.no_input_receiver))).
            then(
                Text('receiver').
                suggests(self._post_manager.order_manager.get_players).
                runs(lambda src, ctx: self._post_manager.post(src, ctx['receiver'])).
                then(
                    GreedyText('comment').
                    runs(lambda src, ctx: self._post_manager.post(src, ctx['receiver'], ctx['comment']))
                )
            )
        )

    def gen_post_list_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.is_player and src.has_permission(self._perm.post)).
            on_error(RequirementNotMet, lambda src: src.reply(
                tr(Tags.no_permission if not src.is_player else Tags.only_for_player)
            ), handled=True).
            runs(lambda src: self.output_post_list(src))
        )

    def gen_receive_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.is_player and src.has_permission(self._perm.receive)).
            on_error(RequirementNotMet, lambda src: src.reply(
                tr(Tags.no_permission if src.is_player else Tags.only_for_player)
            ), handled=True).
            runs(lambda src: src.reply(tr(Tags.no_input_receive_orderid))).
            then(
                Integer('orderid').
                suggests(
                    lambda src: [
                        str(i) for i in
                        self._post_manager.order_manager.get_orderid_by_receiver(src.get_info().player)
                    ]
                ).
                runs(
                    lambda src, ctx: (
                        self._post_manager.receive(src, ctx['orderid']),
                        src.reply(tr(Tags.receive_success, ctx['orderid']))
                    )
                )
            )
        )

    def gen_receive_list_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.is_player and src.has_permission(self._perm.receive)).
            on_error(RequirementNotMet, lambda src: src.reply(
                tr(Tags.no_permission if src.is_player else Tags.only_for_player)
            ), handled=True).
            runs(lambda src: self.output_receive_list(src))
        )

    def gen_cancel_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            requires(lambda src: src.is_player and src.has_permission(self._perm.cancel)).
            on_error(RequirementNotMet, lambda src: src.reply(
                tr(Tags.no_permission if src.is_player else Tags.only_for_player)
            ), handled=True).
            runs(lambda src: src.reply(tr(Tags.no_input_cancel_orderid))).
            then(
                Integer('orderid').
                suggests(
                    lambda src: [
                        str(i) for i in
                        self._post_manager.order_manager.get_orderid_by_sender(src.get_info().player)
                    ]
                ).
                runs(
                    lambda src, ctx: (
                        self._post_manager.receive(src, ctx['orderid']),
                        src.reply(tr(Tags.cancel_success, ctx['orderid']))
                    )
                )
            )
        )

    def gen_list_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name).
            runs(lambda src: src.reply(tr(Tags.command_incomplete))).
            then(
                Literal('players').
                requires(lambda src: src.has_permission(self._perm.list_player)).
                runs(lambda src: src.reply(
                    tr(Tags.list_player_title) + str(self._post_manager.order_manager.get_players())
                ))
            ).
            then(
                Literal('orders').
                requires(lambda src: src.has_permission(self._perm.list_orders)).
                on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
                runs(lambda src: self.output_all_orders(src))
            ).
            then(
                Literal('receive').
                requires(lambda src: src.is_player and src.has_permission(self._perm.receive)).
                on_error(RequirementNotMet, lambda src: src.reply(
                    tr(Tags.no_permission if src.is_player else Tags.only_for_player)
                ), handled=True).
                runs(lambda src: self.output_receive_list(src))
            ).then(
                Literal('post').
                requires(lambda src: src.is_player and src.has_permission(self._perm.post)).
                on_error(RequirementNotMet, lambda src: src.reply(
                    tr(Tags.no_permission if src.is_player else Tags.only_for_player)
                ), handled=True).
                runs(lambda src: self.output_post_list(src))
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
                then(
                    Text('player_id').
                    runs(lambda src, ctx: self._post_manager.order_manager.add_player(ctx['player_id']))
                )
            ).
            then(
                Literal('remove').
                runs(lambda src: src.reply(tr(Tags.command_incomplete))).
                then(
                    Text('player_id').
                    suggests(self._post_manager.order_manager.get_players).
                    runs(lambda src, ctx: self._post_manager.order_manager.remove_player(ctx['player_id']))
                )
            )
        )

    def _gen_save_load_node(self, node_name: str, t: LiteralType["save", "reload"]) -> Literal:
        """生成 save/load 节点

        这两个节点很相似，提取公共部分到这里
        """
        return (
            Literal(node_name).
            requires(lambda src: src.has_permission(getattr(self._perm, t))).
            on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
            runs(getattr(self._post_manager, t)).
            then(
                Literal('all').
                runs(getattr(self._post_manager, t))
            ).
            then(
                Literal('config').
                runs(getattr(self._post_manager.config_manager, t))
            ).
            then(
                Literal('orders').
                runs(getattr(self._post_manager.order_manager, t))
            )
        )

    def gen_save_node(self, node_name: str) -> Literal:
        return self._gen_save_load_node(node_name, 'save')

    def gen_reload_node(self, node_name: str) -> Literal:
        return self._gen_save_load_node(node_name, 'reload')

    def generate_command_node(self, prefix: str) -> Literal:
        """生成指令树"""
        return (
            Literal(prefix).
            requires(lambda src: src.has_permission(self._perm.root)).
            on_error(RequirementNotMet, lambda src: src.reply(tr(Tags.no_permission)), handled=True).
            runs(lambda src: self.output_help_message(src, prefix)).
            then(self.gen_post_node('p')).
            then(self.gen_post_node('post')).
            then(self.gen_post_list_node('pl')).
            then(self.gen_post_list_node('post_list')).
            then(self.gen_receive_node('r')).
            then(self.gen_receive_node('receive')).
            then(self.gen_receive_list_node('rl')).
            then(self.gen_receive_list_node('receive_list')).
            then(self.gen_cancel_node('c')).
            then(self.gen_cancel_node('cancel')).
            then(self.gen_list_node('ls')).
            then(self.gen_list_node('list')).
            then(self.gen_player_node('player')).
            then(self.gen_save_node('save')).
            then(self.gen_reload_node('reload'))
        )


__all__ = ['CommandManager']
