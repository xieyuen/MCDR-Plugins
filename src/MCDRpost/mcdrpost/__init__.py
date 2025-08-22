# -*- coding: utf-8 -*-
"""
插件的入口文件

这里插件会把需要的事件传给 PostManager 处理
"""
from mcdreforged.api.types import PluginServerInterface

from mcdrpost.manager.post_manager import PostManager

manager: PostManager = PostManager(PluginServerInterface.psi())


def on_load(server: PluginServerInterface, prev_module):
    manager.on_load(server, prev_module)


def on_unload(server: PluginServerInterface):
    manager.on_unload(server)

def on_server_startup(server: PluginServerInterface):
    manager.on_server_startup(server)


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    manager.on_server_stop(server, server_return_code)


def on_player_joined(server, player, info):
    manager.on_player_joined(server, player, info)
