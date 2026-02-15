from typing import TYPE_CHECKING

from mcdreforged import InfoCommandSource, RAction, RColor, RText, RTextList

from mcdrpost.constants import END_LINE
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.command_manager import CommandManager
    from mcdrpost.manager.data_manager import DataManager


class CommandHelper:
    def __init__(self, cmd_manager: "CommandManager"):
        self._data_manager: "DataManager" = cmd_manager.data_manager


    # helper methods
    @staticmethod
    def output_help_message(source: InfoCommandSource, prefix: str) -> None:
        """辅助函数：打印帮助信息"""
        msgs_on_helper = RText("")
        msgs_on_admin = RText("")
        if source.has_permission(2):
            # helper以上权限的添加信息
            msgs_on_helper = RTextList(
                RText(prefix + " list orders", RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list orders")
                .h(TranslationKeys.hover.rtr()),
                RText(TranslationKeys.help_info_list_orders.tr() + END_LINE),
            )
        if source.has_permission(3):
            # admin以上权限的添加信息
            msgs_on_admin = RTextList(
                RText(prefix + TranslationKeys.help_usage_player_add.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player add ")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_player_add.tr()}\n"),

                RText(prefix + TranslationKeys.help_usage_player_remove.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player remove ")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_player_remove.tr()}\n"),
            )

        source.reply(
            RTextList(
                RText("--------- §3MCDRpost §r---------\n"),
                RText(TranslationKeys.description.tr() + END_LINE),
                RText(TranslationKeys.help_title.tr() + END_LINE),

                RText(prefix, RColor.gray)
                .c(RAction.suggest_command, prefix)
                .h(TranslationKeys.hover.rtr()),
                RText(f" | {TranslationKeys.help_info_help.tr()}\n"),

                RText(prefix + TranslationKeys.help_usage_post.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} post")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_post.tr()}\n"),

                RText(prefix + " rl", RColor.gray)
                .c(RAction.suggest_command, f"{prefix} receive_list")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_receive_list.tr()}\n"),

                RText(prefix + TranslationKeys.help_usage_receive.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} receive")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_receive.tr()}\n"),

                RText(prefix + " pl", RColor.gray)
                .c(RAction.suggest_command, f"{prefix} post_list")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_post_list.tr()}\n"),

                RText(prefix + TranslationKeys.help_usage_cancel.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} cancel")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_cancel.tr()}\n"),

                RText(prefix + " ls players", RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list players")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_list_players.tr()}\n"),

                msgs_on_helper,
                msgs_on_admin,
                RText("§a『别名 Alias』§r\n"),
                RText("    list -> ls / l\n", RColor.gray),
                RText("    receive -> r\n", RColor.gray),
                RText("    post -> p\n", RColor.gray),
                RText("    cancel -> c\n", RColor.gray),
                RText("-----------------------"),
            )
        )

    def output_post_list(self, src: InfoCommandSource) -> None:
        """辅助函数：输出玩家发送的订单列表"""
        post_list = self._data_manager.get_orders_by_sender(src.get_info().player)

        if not post_list:
            src.reply(TranslationKeys.list_post_none.rtr())
            return

        msg = ""

        for order in post_list:
            msg += (
                f"{order.id}  | {order.receiver}  | {order.time}  | {order.comment}\n"
            )

        src.reply(
            "===========================================\n"
            "{0}\n"
            "{1}"
            "-------------------------------------------\n"
            "{2}"
            "===========================================\n".format(
                TranslationKeys.list_post_title.tr(),
                msg,
                TranslationKeys.list_post_cancel_tip.tr(),
            )
        )

    def output_receive_list(self, src: InfoCommandSource) -> None:
        """辅助函数：输出玩家待接收的邮件列表"""
        receive_list = self._data_manager.get_orders_by_receiver(src.get_info().player)

        if not receive_list:
            src.reply(TranslationKeys.list_receive_none.rtr())
            return

        msg = ""

        for order in receive_list:
            msg += f"{order.id}  | {order.sender}  | {order.time}  | {order.comment}\n"

        src.reply(
            "===========================================\n"
            "{0}\n"
            "{1}\n"
            "-------------------------------------------\n"
            "{2}"
            "===========================================\n".format(
                TranslationKeys.list_receive_title.tr(),
                msg,
                TranslationKeys.list_receive_tip.tr(),
            )
        )

    def output_all_orders(self, src: InfoCommandSource) -> None:
        """辅助函数：输出所有订单列表"""
        all_orders = self._data_manager.get_orders()

        if not all_orders:
            src.reply(TranslationKeys.list_all_none.rtr())
            return

        msg = ""

        for order in all_orders:
            msg += f"{order.id}  | {order.sender}  | {order.receiver}  | {order.time}  | {order.comment}\n"

        src.reply(
            "===========================================\n"
            "{0}\n"
            "{1}\n"
            "===========================================\n".format(
                TranslationKeys.list_all_title.tr(), msg
            )
        )
