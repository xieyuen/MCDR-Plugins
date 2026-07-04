from typing import Self

from mcdreforged import PluginServerInterface
from mcdreforged.constants.plugin_constant import MCDR_PLUGIN_VERSION

from mcdrpost.commands import CommandManager
from mcdrpost.core.services.config_service import ConfigService
from mcdrpost.core.services.data_service import DataService
from mcdrpost.core.services.mcva_service import MCVersionAdaptorService
from mcdrpost.core.services.post_service import PostService


class MCDRpostMain:
    __INSTANCE: Self | None = None

    @classmethod
    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE  # type: ignore

    def __init__(self, server: PluginServerInterface) -> None:
        self.server = server
        self.logger = server.logger

        # initialize services
        self.config_service = ConfigService(server)
        self.data_service = DataService(server, self.config_service)
        self.mcva_service = MCVersionAdaptorService(server)
        self.post_service = PostService(self)

        # initialize managers
        self.command_manager = CommandManager(self)
