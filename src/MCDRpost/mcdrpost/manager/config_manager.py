from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost import constants
from mcdrpost.configuration import Configuration
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.coordinator import MCDRpostCoordinator


class ConfigurationManager:
    """配置管理器"""

    def __init__(self, coo: "MCDRpostCoordinator") -> None:
        self.coo: "MCDRpostCoordinator" = coo
        self._server: PluginServerInterface = coo.server
        self._config: Configuration = self._server.load_config_simple(
            constants.CONFIG_FILE_NAME,
            target_class=Configuration,
            file_format=constants.CONFIG_FILE_TYPE,
            echo_in_console=False
        )

    def reload(self) -> None:
        """(重新)加载配置文件"""
        self._server.logger.info(TranslationKeys.config.load.tr())
        self._config = self._server.load_config_simple(
            constants.CONFIG_FILE_NAME,
            target_class=Configuration,
            file_format=constants.CONFIG_FILE_TYPE,
            echo_in_console=False
        )

    def get_config(self) -> Configuration:
        return self._config
