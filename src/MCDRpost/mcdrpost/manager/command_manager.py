from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost.configuration import CommandPermissions, Configuration
from mcdrpost.constants import SIMPLE_HELP_MESSAGE
from mcdrpost.manager.post_manager import PostManager
from mcdrpost.command.command_helper import CommandHelper
from mcdrpost.command.pre_handler import CommandPreHandler


if TYPE_CHECKING:
    from mcdrpost.coordinator import MCDRpostCoordinator


class CommandManager:
    """命令管理器"""

    def __init__(self, coo: "MCDRpostCoordinator") -> None:
        self.coo: "MCDRpostCoordinator" = coo
        self._post_manager: PostManager = coo.post_manager
        self._server: PluginServerInterface = coo.server
        self.logger = self.coo.logger

        self.data_manager = coo.data_manager
        self._helper = CommandHelper(self)
        self.pre_handler = CommandPreHandler(coo)

    @property
    def _config(self) -> Configuration:
        return self.coo.config

    @property
    def _perm(self) -> CommandPermissions:
        return self._config.permissions

    @property
    def prefixes(self) -> list[str]:
        if self._config.prefix.enable_addition:
            return ["!!po"] + self._config.prefix.more_prefix
        elif self._config.allow_alias:  # TODO: remove in v3.6
            return self._config.command_prefixes
        return ["!!po"]

    def register(self) -> None:
        """注册命令树

        在 on_load 中调用
        """
        for prefix in self.prefixes:
            self._server.register_help_message(prefix, SIMPLE_HELP_MESSAGE)
            self._server.register_command(self.generate_command_node(prefix))
