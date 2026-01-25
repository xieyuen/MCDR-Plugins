from mcdreforged import PluginServerInterface

from mcdrpost.manager.command_manager import CommandManager
from mcdrpost.manager.config_manager import ConfigurationManager
from mcdrpost.manager.data_manager import DataManager
from mcdrpost.manager.event_manager import EventManager
from mcdrpost.manager.post_manager import PostManager
from mcdrpost.manager.version_manager import VersionManager


class MCDRpostCoordinator:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.logger = server.logger

        self.config_manager = ConfigurationManager(self)
        self.data_manager = DataManager(self)
        self.version_manager = VersionManager(server)
        self.post_manager = PostManager(self)
        self.command_manager = CommandManager(self)

        self.event_emitter = EventManager(self)

    @property
    def config(self):
        return self.config_manager.get_config()
