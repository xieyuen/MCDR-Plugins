from mcdreforged import PluginServerInterface

from mcdrpost.utils.mcversion import MCVersion


class Environment:
    def __init__(self, server: PluginServerInterface) -> None:
        self._server = server

    @property
    def _info(self):
        return self._server.get_server_information()

    @property
    def server_version(self) -> MCVersion:
        """Minecraft 服务器版本"""
        return MCVersion(self._info.version)

    @property
    def mcdr_handler(self) -> str:
        """MCDR 正在使用的 handler"""
        return self._server.get_mcdr_config()['handler']


__all__ = ['Environment']
