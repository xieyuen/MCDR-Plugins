from mcdreforged import ServerInterface

from mcdrpost.utils.version import MCVersion


class Environment:
    """Minecraft 版本适配器的环境信息类"""

    mc_version: MCVersion
    """当前运行的 Minecraft 的版本, 若服务器未运行则为 None"""

    def __init__(self, mc_version: MCVersion):
        self.mc_version = mc_version

    @property
    def mcdr_handler(self) -> str:
        """MCDR 所使用的 handler, 这可以代表服务器的核心类型 (e.g. Fabric, Spigot, etc.)"""
        return ServerInterface.si().get_mcdr_config()["handler"]
