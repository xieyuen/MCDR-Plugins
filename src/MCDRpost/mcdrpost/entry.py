"""
插件的入口文件

这里插件会把需要的事件传给 PostManager 处理
"""
from mcdreforged import PluginServerInterface

from mcdrpost.manager.post_manager import PostManager
from mcdrpost.version_handler import register_all_handlers

pm: PostManager = PostManager(PluginServerInterface.psi())
event_emitter = pm.event_manager

register_all_handlers()


def on_load(server: PluginServerInterface, prev_module):
    event_emitter.on_load(server, prev_module)


def on_unload(server: PluginServerInterface):
    event_emitter.on_unload(server)


def on_server_startup(server: PluginServerInterface):
    event_emitter.on_server_startup(server)


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    event_emitter.on_server_stop(server, server_return_code)


def on_player_joined(server, player, info):
    event_emitter.on_player_joined(server, player, info)
