"""
显示服务，用于处理各种命令输出显示
"""
from typing import TYPE_CHECKING

from mcdreforged import CommandSource, InfoCommandSource, RText, RTextList, RColor, RAction

from mcdrpost.constants import END_LINE
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class DisplayService:
    """显示服务，用于处理各种命令输出显示"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager = post_manager
        self._data_manager = post_manager.data_manager
        self._config = post_manager.configuration

    def output_help_message(self, source: CommandSource, prefix: str) -> None:
        """打印帮助信息"""
        msgs_on_helper = RText('')
        msgs_on_admin = RText('')
        if source.has_permission(2):
            # helper以上权限的添加信息
            msgs_on_helper = RTextList(
                RText(prefix + ' list orders', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list orders")
                .h(TranslationKeys.hover.tr()),

                RText(TranslationKeys.help.hint_ls_orders.tr() + END_LINE),
            )
        if source.has_permission(3):
            # admin以上权限的添加信息
            msgs_on_admin = RTextList(
                RText(prefix + TranslationKeys.help.player_add.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player add ")
                .h(TranslationKeys.hover.tr()), RText(f'{TranslationKeys.help.hint_player_add.tr()}\n'),

                RText(prefix + TranslationKeys.help.player_remove.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player remove ")
                .h(TranslationKeys.hover.tr()), RText(f'{TranslationKeys.help.hint_player_remove.tr()}\n'),
            )

        source.reply(
            RTextList(
                RText('--------- §3MCDRpost §r---------\n'),
                RText(TranslationKeys.desc.tr() + END_LINE),
                RText(TranslationKeys.help.title.tr() + END_LINE),
                RText(prefix, RColor.gray).c(RAction.suggest_command, prefix).h(TranslationKeys.hover.tr()),
                RText(f' | {TranslationKeys.help.hint_help.tr()}\n'),
                RText(prefix + TranslationKeys.help.p.tr(), RColor.gray).c(RAction.suggest_command, f"{prefix} post").h(
                    TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_p.tr()}\n'),
                RText(prefix + ' rl', RColor.gray).c(RAction.suggest_command, f"{prefix} receive_list").h(TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_rl.tr()}\n'),
                RText(prefix + TranslationKeys.help.r.tr(), RColor.gray).c(RAction.suggest_command, f"{prefix} receive").h(
                    TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_r.tr()}\n'),
                RText(prefix + ' pl', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} post_list").h(TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_pl.tr()}\n'),
                RText(prefix + TranslationKeys.help.c.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} cancel").h(TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_c.tr()}\n'),
                RText(prefix + ' ls players', RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list players").h(TranslationKeys.hover.tr()),
                RText(f'{TranslationKeys.help.hint_ls_players.tr()}\n'),
                msgs_on_helper,
                msgs_on_admin,
                RText("§a『别名 Alias』§r\n"),
                RText("    list -> ls 或 l\n", RColor.gray),
                RText("    receive -> r\n", RColor.gray),
                RText("    post -> p\n", RColor.gray),
                RText("    cancel -> c\n", RColor.gray),
                RText(f'根指令: {", ".join(self._post_manager.command_manager.get_prefixes())}\n'),
                RText('-----------------------'),
            )
        )

    def output_post_list(self, src: InfoCommandSource) -> None:
        """输出玩家发送的订单列表"""
        post_list = self._data_manager.get_orders_by_sender(
            src.get_info().player
        )

        if not post_list:
            src.reply(TranslationKeys.no_post_orders.tr())
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
            .format(TranslationKeys.list_post_orders_title.tr(), msg, TranslationKeys.hint_cancel.tr())
        )

    def output_receive_list(self, src: InfoCommandSource) -> None:
        """输出玩家待接收的邮件列表"""
        receive_list = self._data_manager.get_orders_by_receiver(
            src.get_info().player
        )

        if not receive_list:
            src.reply(TranslationKeys.no_receive_orders.tr())
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
            .format(TranslationKeys.list_receive_orders_title.tr(), msg, TranslationKeys.hint_order_receive.tr())
        )

    def output_all_orders(self, src: InfoCommandSource) -> None:
        """输出所有订单列表"""
        all_orders = self._data_manager.get_orders()

        if not all_orders:
            src.reply(TranslationKeys.no_orders.tr())
            return

        msg = ""

        for order in all_orders:
            msg += f"{order.id}  | {order.sender}  | {order.receiver}  | {order.time}  | {order.comment}\n"

        src.reply(
            '===========================================\n'
            '{0}\n'
            '{1}\n'
            '===========================================\n'
            .format(TranslationKeys.list_orders_title.tr(), msg)
        )