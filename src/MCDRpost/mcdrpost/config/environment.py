from mcdreforged.api.types import PluginServerInterface

from mcdrpost.utils import tr
from mcdrpost.utils.translation_tags import Tags


class Environment:
    def __init__(self, server: PluginServerInterface) -> None:
        self._server = server

    @property
    def server_version(self) -> str | None:
        return self._server.get_server_information().version

    def item_command(self) -> bool:
        """``item`` 命令是否可用

        在 Minecraft 1.17 之后，``replaceitem`` 命令被 ``item replace``代替
        这会影响到插件替换手中物品时执行的 Minecraft 命令
        """
        if self.server_version is None:
            self._server.logger.warning(tr(Tags.env.server_no_start))
            return True
        return self.server_version >= "1.17"


__all__ = ['Environment']
