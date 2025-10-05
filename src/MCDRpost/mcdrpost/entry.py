"""
插件的入口文件

这里插件会把需要的事件传给 PostManager 处理
"""
from mcdreforged import PluginServerInterface

from mcdrpost.mcdrpost_coordinator import MCDRpostCoordinator
from mcdrpost.version_handler import register_builtin_handlers

coordinator: MCDRpostCoordinator

register_builtin_handlers()


def on_load(server: PluginServerInterface, prev_module):
    global coordinator
    coordinator = MCDRpostCoordinator(server)
    coordinator.event_emitter.on_load(server, prev_module)


def on_unload(server: PluginServerInterface):
    coordinator.event_emitter.on_unload(server)


def on_server_startup(server: PluginServerInterface):
    coordinator.event_emitter.on_server_startup(server)


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    coordinator.event_emitter.on_server_stop(server, server_return_code)


def on_player_joined(server, player, info):
    coordinator.event_emitter.on_player_joined(server, player, info)
