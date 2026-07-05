import importlib

from mcdreforged import MCDRPluginEvents, PluginServerInterface, event_listener

from mcdrpost.constants import BUILTIN_ADAPTORS_PATH
from mcdrpost.data_structure import Item
from mcdrpost.mcva.abstract_adaptor import AbstractMCVersionAdaptor, BuiltinAdaptor
from mcdrpost.mcva.environment import Environment
from mcdrpost.utils.version import MCVersion


class MCVersionAdaptorService:
    __builtin_adapters__: list[BuiltinAdaptor] = []
    __external_adapters__: list[AbstractMCVersionAdaptor] = []

    @classmethod
    def register_adaptor(cls, adaptor: AbstractMCVersionAdaptor) -> None:
        if not isinstance(adaptor, AbstractMCVersionAdaptor):
            raise TypeError(f"Invalid adaptor: {adaptor}")

        if adaptor.is_builtin():
            assert isinstance(adaptor, BuiltinAdaptor)
            cls.__builtin_adapters__.append(adaptor)
        else:
            cls.__external_adapters__.append(adaptor)

    def __init__(self, server: PluginServerInterface) -> None:
        self.server = server
        self.logger = server.logger

        self.logger.debug(f"initializing MCVA service")
        self.__register_builtin_adaptors()
        self.current_adaptor: AbstractMCVersionAdaptor | None = None
        """当前选中的适配器实例, 在服务器启动时根据版本自动选择"""

    def __register_builtin_adaptors(self) -> None:
        """自动导入 version_handler/impl 目录下所有模块

        通过动态导入所有版本处理器模块，触发它们的自动注册机制
        """
        self.logger.debug(f"registering builtin adapters")

        for file_path in BUILTIN_ADAPTORS_PATH.glob("*.py"):
            # 动态导入模块，触发其中的注册代码
            importlib.import_module(f"mcdrpost.mcva.impl.{file_path.stem}")

    @event_listener(MCDRPluginEvents.SERVER_STARTUP)
    def on_server_startup(self, server: PluginServerInterface):
        self.logger.debug("selecting correct adaptor for server")

        mcv = server.get_server_information().version
        assert mcv is not None, "invalid server version"

        env = Environment(MCVersion(mcv))

        for adaptor in self.__external_adapters__:
            if adaptor.is_usable(env):
                self.current_adaptor = adaptor
                self.logger.info(f"selected external adaptor: {adaptor}")
                return

        self.logger.debug(f"no external adaptor selected")
        self.logger.debug(f"selecting builtin adaptors")

        for adaptor in self.__builtin_adapters__:
            if adaptor.is_usable(env):
                self.current_adaptor = adaptor
                self.logger.info(f"selected builtin adaptor: {adaptor}")
                return

        raise RuntimeError("No adaptor selected")

    def replace(self, player: str, item: Item) -> None:
        """替换某人的副手物品"""
        self.server.execute(self.current_adaptor.get_replace_command(player, item))

    def get_offhand_item(self, player: str) -> Item:
        """获取玩家副手物品, 应该在非 TaskExecutor 线程运行"""
        if self.server.is_on_executor_thread():
            raise RuntimeError('Cannot invoke get_offhand_item on the task executor thread')
        return self.current_adaptor.get_offhand_item(player)
