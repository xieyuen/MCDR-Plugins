from mcdreforged import PluginServerInterface

from mcdrpost.utils.version import SemanticVersion


class Environment:
    def __init__(self, server: PluginServerInterface) -> None:
        self._server = server

    @property
    def _info(self):
        return self._server.get_server_information()

    @property
    def server_version(self) -> SemanticVersion | None:
        """Minecraft 服务器版本"""
        if self._info.version is None:
            return None
        return SemanticVersion(self._info.version)

    @property
    def mcdr_handler(self) -> str:
        """MCDR 正在使用的 handler"""
        return self._server.get_mcdr_config()['handler']


__all__ = ['Environment']
