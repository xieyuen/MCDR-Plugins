from typing import cast

from mcdreforged import Literal, Text, GreedyText, Integer, InfoCommandSource, RequirementNotMet, CommandSource

from mcdrpost.command.command_helper import CommandHelper
from mcdrpost.utils.node_addition import add_requirements
from mcdrpost.utils.translation import TranslationKeys


class CmdNodeGenerator:
    def __init__(self, ):
        self._helper = CommandHelper()

    def gen_post_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name)
            .runs(lambda src: src.reply(TranslationKeys.post_fail_receiver_unregistered.rtr()))
            .then(
                Text("receiver")
                .suggests(self.data_manager.get_players)
                .runs(self.pre_handler.post)
                .then(GreedyText("comment").runs(self.pre_handler.post))
            ),
            permission=self._perm.post,
            require_player=True,
        )

    def gen_post_list_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).runs(lambda src: self._helper.output_post_list(src)),
            permission=self._perm.post,
            require_player=True,
        )

    def gen_receive_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name)
            .runs(lambda src: src.reply(TranslationKeys.receive_fail_undefined_id.rtr()))
            .then(
                Integer("orderid")
                .suggests(
                    lambda src: [
                        str(i)
                        for i in self.data_manager.get_orderid_by_receiver(
                            src.get_info().player
                        )
                    ]
                )
                .runs(self.pre_handler.receive)
            ),
            permission=self._perm.receive,
            require_player=True,
        )

    def gen_receive_list_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name).runs(
                lambda src: self._helper.output_receive_list(
                    cast(InfoCommandSource, src)
                )
            ),
            permission=self._perm.receive,
            require_player=True,
        )

    def gen_cancel_node(self, node_name: str) -> Literal:
        return add_requirements(
            Literal(node_name)
            .runs(lambda src: src.reply(TranslationKeys.cancel_fail_undefined_id.tr()))
            .then(
                Integer("orderid")
                .suggests(
                    lambda src: [
                        str(i)
                        for i in self.data_manager.get_orderid_by_sender(
                            src.get_info().player
                        )
                    ]
                )
                .runs(self.pre_handler.cancel)
            ),
            permission=self._perm.cancel,
            require_player=True,
        )

    def gen_list_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name)
            .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.tr()))
            .then(
                Literal("players")
                .requires(lambda src: src.has_permission(self._perm.list_player))
                .runs(
                    lambda src: src.reply(
                        TranslationKeys.list_players_title.tr()
                        + str(self.data_manager.get_players())
                    )
                )
            )
            .then(
                Literal("orders")
                .requires(lambda src: src.has_permission(self._perm.list_orders))
                .on_error(
                    RequirementNotMet,
                    lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                    handled=True,
                )
                .runs(
                    lambda src: self._helper.output_all_orders(
                        cast(InfoCommandSource, src)
                    )
                )
            )
            .then(
                add_requirements(
                    Literal("receive").runs(
                        lambda src: self._helper.output_receive_list(
                            cast(InfoCommandSource, src)
                        )
                    ),
                    permission=self._perm.receive,
                    require_player=True,
                )
            )
            .then(
                add_requirements(
                    Literal("post").runs(
                        lambda src: self._helper.output_post_list(
                            cast(InfoCommandSource, src)
                        )
                    ),
                    permission=self._perm.post,
                    require_player=True,
                )
            )
        )

    def gen_player_node(self, node_name: str) -> Literal:
        return (
            Literal(node_name)
            .requires(lambda src: src.has_permission(self._perm.player))
            .on_error(
                RequirementNotMet,
                lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                handled=True,
            )
            .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.rtr()))
            .then(
                Literal("add")
                .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.rtr()))
                .then(Text("player_id").runs(self.pre_handler.add_player))
            )
            .then(
                Literal("remove")
                .runs(lambda src: src.reply(TranslationKeys.error_incomplete_general.rtr()))
                .then(
                    Text("player_id")
                    .suggests(self.data_manager.get_players)
                    .runs(self.pre_handler.remove_player)
                )
            )
        )

    def gen_reload_node(self, prefix) -> Literal:
        """deprecated in 2026.2.15"""

        def reload(src: CommandSource):
            self.coo.config_manager.reload()
            self.coo.data_manager.reload()
            src.reply(TranslationKeys.config_reloaded.rtr())
            src.reply(TranslationKeys.data_loaded.rtr())

        return (
            Literal(prefix)
            .requires(lambda src: src.has_permission(self._perm.reload))
            .on_error(
                RequirementNotMet,
                lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                handled=True,
            )
            .runs(reload)
        )

    def generate_command_node(self, prefix: str) -> Literal:
        """生成指令树"""
        return (
            Literal(prefix)
            .requires(lambda src: src.has_permission(self._perm.root))
            .on_error(
                RequirementNotMet,
                lambda src: src.reply(TranslationKeys.error_no_perm.rtr()),
                handled=True,
            )
            .runs(lambda src: self._helper.output_help_message(src, prefix))
            # 下面的一行就是一条命令，多个 then 意味着别名/缩写
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
            # .then(self.gen_reload_node("reload"))
        )
