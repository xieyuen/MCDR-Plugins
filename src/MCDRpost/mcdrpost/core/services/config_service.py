from typing import Literal

from mcdreforged import PluginServerInterface

from mcdrpost.config import Configuration
from mcdrpost.utils.translation import TranslationKeys


class ConfigService:
    CONFIG_FILE = "config.yml"
    CONFIG_TYPE: Literal["yaml"] = "yaml"

    @property
    def config(self):
        return self._config

    def __init__(self, server: PluginServerInterface):
        self.server = server
        self._config = server.load_config_simple(
            self.CONFIG_FILE,
            target_class=Configuration,
            in_data_folder=True,
            echo_in_console=True,
            file_format=self.CONFIG_TYPE,
        )

    def reload(self):
        self._config = self.server.load_config_simple(
            self.CONFIG_FILE,
            target_class=Configuration,
            in_data_folder=True,
            echo_in_console=False,
            file_format=self.CONFIG_TYPE,
        )
        self.server.logger.info(TranslationKeys.config_reloaded.rtr())
