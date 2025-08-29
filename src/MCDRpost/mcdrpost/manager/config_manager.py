from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost import constants
from mcdrpost.configuration import Configuration
from mcdrpost.utils.translation import Tags, tr

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager  # noqa: F401


class ConfigurationManager:
    """配置管理器

    Attributes:
        configuration (Configuration): 插件配置
    """

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager: "PostManager" = post_manager
        self._server: PluginServerInterface = post_manager.server
        self.configuration: Configuration = self._server.load_config_simple(
            constants.CONFIG_FILE_NAME,
            target_class=Configuration,
            file_format=constants.CONFIG_FILE_TYPE,
        )

    def reload(self) -> None:
        self._server.logger.info(tr(Tags.config.load))
        self.configuration = self._server.load_config_simple(
            constants.CONFIG_FILE_NAME,
            target_class=Configuration,
            file_format=constants.CONFIG_FILE_TYPE,
        )

    def save(self) -> None:
        self._server.logger.info(tr(Tags.config.save))
        self._server.save_config_simple(
            self.configuration,
            constants.CONFIG_FILE_NAME,
            file_format=constants.CONFIG_FILE_TYPE
        )

    def get_configuration(self) -> Configuration:
        return self.configuration


__all__ = ['ConfigurationManager']
