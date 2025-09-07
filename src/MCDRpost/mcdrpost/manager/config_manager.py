from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost import constants
from mcdrpost.configuration import Configuration
from mcdrpost.utils.translation import Tags, tr

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager  # noqa: F401


class ConfigurationManager:
    """配置管理器"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager: "PostManager" = post_manager
        self._server: PluginServerInterface = post_manager.server
        self._configuration: Configuration | None = None

    def reload(self) -> None:
        """(重新)加载配置文件"""
        self._server.logger.info(tr(Tags.config.load))
        self._configuration = self._server.load_config_simple(
            constants.CONFIG_FILE_NAME,
            target_class=Configuration,
            file_format=constants.CONFIG_FILE_TYPE,
        )

    def get_configuration(self) -> Configuration:
        return self._configuration


__all__ = ['ConfigurationManager']
