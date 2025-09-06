from mcdreforged import PluginServerInterface


class Environment:
    def __init__(self, server: PluginServerInterface) -> None:
        self._server = server

    @property
    def server_version(self) -> str | None:
        """Minecraft 服务器版本"""
        return self._server.get_server_information().version

    @property
    def mcdr_handler(self) -> str:
        """MCDR 正在使用的 handler"""
        return self._server.get_mcdr_config()['handler']


__all__ = ['Environment']
