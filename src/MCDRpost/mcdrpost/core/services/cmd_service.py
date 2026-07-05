from typing import TYPE_CHECKING

from mcdrpost.commands.cmd_tree import CommandTree
from mcdrpost.config import CommandPermissions, Configuration

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class CommandService:
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
        self.cmd_tree = CommandTree(mcdrpost)

    def register_command_tree(self):
        raise NotImplementedError
