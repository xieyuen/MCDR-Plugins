from mcdreforged import PluginServerInterface


class Environment:
    def __init__(self, server: PluginServerInterface) -> None:
        self._server = server

    @property
    def server_version(self) -> str | None:
        return self._server.get_server_information().version


__all__ = ['Environment']
