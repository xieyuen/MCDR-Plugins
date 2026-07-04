from typing import TYPE_CHECKING, cast

from mcdreforged import (
    CommandContext,
    CommandSource,
    GreedyText,
    InfoCommandSource,
    Integer,
    Literal,
    PlayerCommandSource,
    RequirementNotMet,
    Text,
)
from mcdreforged import RAction, RColor, RText, RTextList

from mcdrpost.constants import END_LINE, SIMPLE_HELP_MESSAGE
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class CommandManager:
    """命令管理器"""

    def __init__(self, mcdrpost: "MCDRpostMain") -> None:
        self.mcdrpost = mcdrpost
        self.server = mcdrpost.server
        self.logger = mcdrpost.logger
        self.post_service = mcdrpost.post_service
        self.data_service = mcdrpost.data_service

    @property
    def config(self):
        return self.mcdrpost.config_service.config

    @property
    def perm(self):
        return self.config.permissions

    @property
    def prefixes(self) -> list[str]:
        if self.config.prefix.enable_addition:
            return ["!!po"] + self.config.prefix.more_prefix
        return ["!!po"]

    def register(self) -> None:
        """注册命令树"""
        for prefix in self.prefixes:
            self.server.register_help_message(prefix, SIMPLE_HELP_MESSAGE)
            self.server.register_command(self.generate_command_node(prefix))

    # 辅助方法
    def output_help_message(self, source: InfoCommandSource, prefix: str) -> None:
        """输出帮助信息"""
        msgs_on_helper = RText("")
        msgs_on_admin = RText("")

        if source.has_permission(2):
            msgs_on_helper = RTextList(
                RText(prefix + " list orders", RColor.gray)
                .c(RAction.suggest_command, f"{prefix} list orders")
                .h(TranslationKeys.hover.rtr()),
                RText(TranslationKeys.help_info_list_orders.tr() + END_LINE),
            )

        if source.has_permission(3):
            msgs_on_admin = RTextList(
                RText(prefix + TranslationKeys.help_usage_player_add.tr(), RColor.gray)
                .c(RAction.suggest_command, f"{prefix} player add ")
                .h(TranslationKeys.hover.rtr()),
                RText(f"{TranslationKeys.help_info_player_add.tr()}\n"),
                RText(
                    prefix + TranslationKeys.help_usage_player_remove.tr(), RColor.gray
                )
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
        """输出玩家发送的订单列表"""
        post_list = self.data_service.get_orders_by_sender(src.get_info().player)
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
        """输出玩家待接收的邮件列表"""
        receive_list = self.data_service.get_orders_by_receiver(src.get_info().player)
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
        """输出所有订单列表"""
        all_orders = self.data_service.get_all_orders()
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

    # 命令处理函数
    def post_handler(self, src: CommandSource, ctx: CommandContext):
        """发送邮件命令处理"""
        receiver = ctx["receiver"]
        comment = ctx.get("comment")
        self.post_service.post(cast(PlayerCommandSource, src), receiver, comment)

    def receive_handler(self, src: CommandSource, ctx: CommandContext):
        """接收邮件命令处理"""
        order_id = ctx["orderid"]
        if self.post_service.receive(cast(PlayerCommandSource, src), order_id):
            src.reply(TranslationKeys.receive_success.tr(order_id))

    def cancel_handler(self, src: CommandSource, ctx: CommandContext):
        """取消邮件命令处理"""
        order_id = ctx["orderid"]
        if self.post_service.cancel(cast(PlayerCommandSource, src), order_id):
            src.reply(TranslationKeys.cancel_success.tr(order_id))

    def add_player_handler(self, src: CommandSource, ctx: CommandContext):
        """添加玩家命令处理"""
        player = ctx["player_id"]
        if not self.data_service.add_player(player):
            src.reply(TranslationKeys.player_fail_already_registered.rtr(player))
            return
        src.reply(TranslationKeys.player_registered.rtr(player))
        self.logger.info(TranslationKeys.data_auto_register.rtr(player))
        self.data_service.save()

    def remove_player_handler(self, src: CommandSource, ctx: CommandContext):
        """移除玩家命令处理"""
        player = ctx["player_id"]
        if not self.data_service.remove_player(player):
            src.reply(TranslationKeys.player_fail_unable_del.rtr(player))
            return
        src.reply(TranslationKeys.player_removed.rtr(player))
        self.logger.info(TranslationKeys.player_removed.rtr(player))
        self.data_service.save()

    # 命令节点生成
    def _add_requirements(self, node, permission: int, require_player: bool = False):
        """添加权限和玩家要求"""
        if require_player:
            node.requires(
                lambda src: src.is_player,
                lambda: TranslationKeys.error_player_only.rtr(),
            )
        node.requires(
            lambda src: src.has_permission(permission),
            lambda: TranslationKeys.error_no_perm.rtr(),
        )
        return node

    def gen_post_node(self, node_name: str) -> Literal:
        """生成发送邮件命令节点"""
        return self._add_requirements(
            Literal(node_name)
            .runs(
                lambda src: src.reply(
                    TranslationKeys.error_incomplete_receiver.rtr()
                )
            )
            .then(
                Text("receiver")
                .suggests(lambda src: self.data_service.get_players())
                .runs(self.post_handler)
                .then(GreedyText("comment").runs(self.post_handler))
            ),
            permission=self.perm.post,
            require_player=True,
        )

    def gen_post_list_node(self, node_name: str) -> Literal:
        """生成发送列表命令节点"""
        return self._add_requirements(
            Literal(node_name).runs(
                lambda src: self.output_post_list(cast(InfoCommandSource, src))
            ),
            permission=self.perm.post,
            require_player=True,
        )

    def gen_receive_node(self, node_name: str) -> Literal:
        """生成接收邮件命令节点"""
        return self._add_requirements(
            Literal(node_name)
            .runs(
                lambda src: src.reply(TranslationKeys.error_incomplete_order_id.rtr())
            )
            .then(
                Integer("orderid")
                .suggests(
                    lambda src: [
                        str(i)
                        for i in self.data_service.get_orderid_by_receiver(
                            src.get_info().player
                        )
                    ]
                )
                .runs(self.receive_handler)
            ),
            permission=self.perm.receive,
            require_player=True,
        )

    def gen_receive_list_node(self, node_name: str) -> Literal:
        """生成接收列表命令节点"""
        return self._add_requirements(
            Literal(node_name).runs(
                lambda src: self.output_receive_list(cast(InfoCommandSource, src))
            ),
            permission=self.perm.receive,
            require_player=True,
        )

    def gen_cancel_node(self, node_name: str) -> Literal:
        """生成取消邮件命令节点"""
        return self._add_requirements(
            Literal(node_name)
            .runs(
                lambda src: src.reply(TranslationKeys.error_incomplete_order_id.rtr())
            )
            .then(
                Integer("orderid")
                .suggests(
                    lambda src: [
                        str(i)
                        for i in self.data_service.get_orderid_by_sender(
                            src.get_info().player
                        )
                    ]
                )
                .runs(self.cancel_handler)
            ),
            permission=self.perm.cancel,
            require_player=True,
        )

    def gen_list_node(self, node_name: str) -> Literal:
        """生成列表命令节点"""
        return (
            Literal(node_name)
            .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.tr()))
            .then(
                Literal("players")
                .requires(lambda src: src.has_permission(self.perm.list_player))
                .on_error(
                    RequirementNotMet,
                    lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                    handled=True,
                )
                .runs(
                    lambda src: src.reply(
                        TranslationKeys.list_players_title.tr()
                        + str(self.data_service.get_players())
                    )
                )
            )
            .then(
                Literal("orders")
                .requires(lambda src: src.has_permission(self.perm.list_orders))
                .on_error(
                    RequirementNotMet,
                    lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                    handled=True,
                )
                .runs(
                    lambda src: self.output_all_orders(
                        cast(InfoCommandSource, src)
                    )
                )
            )
            .then(
                self._add_requirements(
                    Literal("receive").runs(
                        lambda src: self.output_receive_list(
                            cast(InfoCommandSource, src)
                        )
                    ),
                    permission=self.perm.receive,
                    require_player=True,
                )
            )
            .then(
                self._add_requirements(
                    Literal("post").runs(
                        lambda src: self.output_post_list(
                            cast(InfoCommandSource, src)
                        )
                    ),
                    permission=self.perm.post,
                    require_player=True,
                )
            )
        )

    def gen_player_node(self, node_name: str) -> Literal:
        """生成玩家管理命令节点"""
        return (
            Literal(node_name)
            .requires(lambda src: src.has_permission(self.perm.player))
            .on_error(
                RequirementNotMet,
                lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                handled=True,
            )
            .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.rtr()))
            .then(
                Literal("add")
                .runs(
                    lambda src: src.reply(
                        TranslationKeys.error_incomplete_general.rtr()
                    )
                )
                .then(Text("player_id").runs(self.add_player_handler))
            )
            .then(
                Literal("remove")
                .runs(
                    lambda src: src.reply(
                        TranslationKeys.error_incomplete_general.rtr()
                    )
                )
                .then(
                    Text("player_id")
                    .suggests(lambda src: self.data_service.get_players())
                    .runs(self.remove_player_handler)
                )
            )
        )

    def generate_command_node(self, prefix: str) -> Literal:
        """生成指令树"""
        return (
            Literal(prefix)
            .requires(lambda src: src.has_permission(self.perm.root))
            .on_error(
                RequirementNotMet,
                lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                handled=True,
            )
            .runs(lambda src: self.output_help_message(cast(InfoCommandSource, src), prefix))
            .then(self.gen_post_node("p"))
            .then(self.gen_post_node("post"))
            .then(self.gen_post_list_node("pl"))
            .then(self.gen_post_list_node("post_list"))
            .then(self.gen_receive_node("r"))
            .then(self.gen_receive_node("receive"))
            .then(self.gen_receive_list_node("rl"))
            .then(self.gen_receive_list_node("receive_list"))
            .then(self.gen_cancel_node("c"))
            .then(self.gen_cancel_node("cancel"))
            .then(self.gen_list_node("ls"))
            .then(self.gen_list_node("list"))
            .then(self.gen_player_node("player"))
        )
