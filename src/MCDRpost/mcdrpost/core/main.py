from mcdreforged import PluginServerInterface

from mcdrpost.core.services.config_service import ConfigService
from mcdrpost.core.services.data_service import DataService


class MCDRpostMain:
    def __init__(self, server: PluginServerInterface) -> None:
        self.server = server
        self.logger = server.logger

        # initialize services
        self.config_service = ConfigService(server)
        self.data_service = DataService(server, self.config_service)
