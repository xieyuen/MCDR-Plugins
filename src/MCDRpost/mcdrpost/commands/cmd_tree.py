from typing import TYPE_CHECKING

from mcdreforged import Literal, RequirementNotMet, Text

from mcdrpost.commands import cmd_tools
from mcdrpost.config import CommandPermissions, Configuration
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class CommandTree:
    @property
    def config(self) -> Configuration:
        return self.mcdrpost.config_service.config

    @property
    def perm(self) -> CommandPermissions:
        return self.config.permissions

    def __init__(self, mcdrpost: "MCDRpostMain"):
        mcdrpost.logger.info("Initializing CommandService")
        self.mcdrpost = mcdrpost
        self.server = mcdrpost.server
        self.logger = mcdrpost.logger

    def generate_cmdtree(self, prefix: str) -> Literal:
        return (
            Literal(prefix)
            .then(self.post_node("post"))
        )

    def post_node(self, node: str) -> Literal:
        return (
            Literal(node)
            .precondition(cmd_tools.require_perm(self.perm.post))
            .requires(cmd_tools.require_player)
            .on_error(RequirementNotMet, cmd_tools.cannot_used_by_console, handled=True)
            .runs(cmd_tools.reply_incomplete_cmd)
            .then(
                Text("receiver")
                .suggests(self.mcdrpost.data_service.get_players)
                .runs()
            )
        )
