from mcdreforged import MCDRPluginEvents, PluginEvent, PluginServerInterface
from mcdreforged.plugin.plugin_event import MCDREvent


class ServerEvent(PluginEvent):
    """服务器事件, 包括服务端控制等"""

    def __init__(self, event_id: str) -> None:
        super().__init__(event_id)

    @classmethod
    def is_server_event(cls, e: PluginEvent) -> bool:
        return isinstance(e, cls)


class _ServerEventStorage:
    EVENT_DICT: dict[str, MCDREvent | ServerEvent] = {}

    @classmethod
    def register(cls, event: MCDREvent | ServerEvent):
        if event.id in cls.EVENT_DICT:
            raise KeyError(event.id)
        cls.EVENT_DICT[event.id] = event

    @classmethod
    def get_mcdr_event(cls) -> list[MCDREvent]:
        return [e for e in cls.EVENT_DICT.values() if isinstance(e, MCDREvent)]

    @classmethod
    def get_server_event(cls) -> list[ServerEvent]:
        return [e for e in cls.EVENT_DICT.values() if isinstance(e, ServerEvent)]


class ServerEvents:
    """装有全部服务器生命周期/控制事件的常量类

    该类包含 MCDR 内置的服务器生命周期事件和本插件定义的全部服务器控制事件.
    所有的 MCDR 内置声明周期事件均为 MCDREvent 实例,
    所有的自定义事件均为 ServerEvent 实例.

    See Also:
        MCDR 官方文档:

        - https://docs.mcdreforged.com/zh-cn/latest/plugin_dev/event.html
        - https://docs.mcdreforged.com/zh-cn/latest/code_references/ServerInterface.html#server-control
    """

    # Server Controlling Events

    # Server starting
    SERVER_PRE_STARTING: MCDREvent = MCDRPluginEvents.SERVER_START_PRE
    """服务器准备启动"""
    SERVER_STARTING: MCDREvent = MCDRPluginEvents.SERVER_START
    """服务器正在启动"""
    SERVER_STARTED: MCDREvent = MCDRPluginEvents.SERVER_STARTUP
    """服务器已启动"""
    # Server Stopping
    SERVER_STOPPING: ServerEvent = ServerEvent("kill_server.server_stopping")
    """服务器正在停止"""
    PLUGIN_STOPPING_SERVER: ServerEvent = ServerEvent("kill_server.plugin_stopping_server")
    """服务器正在被插件/MCDR命令关闭
    
    当且仅当 :meth:`mcdreforged.plugin.si.ServerInterface.stop` 调用时触发
    """
    PLUGIN_KILLING_SERVER: ServerEvent = ServerEvent("kill_server.plugin_killing_server")
    """服务器正在被插件/MCDR命令强制关闭
    
    当且仅当 :meth:`mcdreforged.plugin.si.ServerInterface.kill` 调用时触发
    """
    SERVER_STOPPED: MCDREvent = MCDRPluginEvents.SERVER_STOP
    """服务器已停止"""

    WORLD_SAVED: ServerEvent = ServerEvent("kill_server.world_saved")
    """世界已保存"""

    # Methods
    @classmethod
    def get_event_list(cls) -> list[MCDREvent | ServerEvent]:
        """:meta private:"""
        return list(_ServerEventStorage.EVENT_DICT.values())

    @classmethod
    def contains_id(cls, event_id: str) -> bool:
        """:meta private:"""
        return event_id in _ServerEventStorage.EVENT_DICT


def __register_server_events():
    for name, value in vars(ServerEvents).items():
        if not name.startswith('_') and isinstance(value, MCDREvent | ServerEvent):
            _ServerEventStorage.register(value)


__register_server_events()


def dispatch(event: PluginEvent, args: tuple = ()):
    """以指定参数分发事件"""
    PluginServerInterface.psi().dispatch_event(event, args)
