# -*- coding: utf-8 -*-

import time

from typing import Dict

from mcdreforged.api.types import PluginServerInterface as mcdrserver
from mcdreforged.api.command import *
from mcdreforged.api.utils import Serializable
from dict_command_registration import NodeType, register

class Config(Serializable):
    permissions: Dict[str, int] = {
        'help': 3,
        'start': 3,
        'stop': 3,
        'stop_exit': 4,
        'restart': 3,
        'exit': 4,
        'kill': 4,
    }


config: Config

command = {
    'name': '!!server',
    'requires': "permissions['help']",
    'runs': "src.reply(server.rtr('start_stop_helper_r.help'))",
    'children': [
        {
            'name': 'start',
            'requires': "permissions['start']",
            'runs': 'server.start()'
        },
        {
            'name': 'stop',
            'requires': "permissions['stop']",
            'runs': 'stop_server()'
        },
        {
            'name': 'restart',
            'requires': "permissions['restart']",
            'runs': 'server.restart()'
        },
        {
            'name': 'stop_exit',
            'requires': "permissions['stop_exit']",
            'runs': 'stop_exit_server()'
        },
        {
            'name': 'kill',
            'requires': "permissions['kill']",
            'runs': 'server.kill()'
        },
        {
            'name': 'exit',
            'requires': "permissions['exit']",
            'runs': 'server.exit()'
        },
    ]
}


def stop_server():

    mcdrserver.stop()
    time.sleep(10)

    if server.is_server_running() == True:
        time.sleep(60)
        if mcdrserver.is_server_running() == True:

            mcdrserver.logger.warning("服务器似乎并没有关闭...")
            mcdrserver.logger.info("10s后服务端进程将被杀死.")
            time.sleep(10)
            mcdrserver.set_exit_after_stop_flag(False)
            if mcdrserver.is_server_running() == False:
                mcdrserver.logger.info("服务端已关闭")
            else:
                mcdrserver.set_exit_after_stop_flag(False)
                mcdrserver.kill()

    mcdrserver.logger.info("服务端已关闭.")


def stop_exit_server():
    stop_server()
    mcdrserver.exit()


def restart_server():
    stop_server()
    mcdrserver.start()


def on_load(server: mcdrserver, prev_module):
    global config
    config = server.load_config_simple('config.json', target_class=Config)
    permissions = config.permissions
    server.logger.info("插件已加载")
    server.logger.warning("你使用的并非原版！而是 xieyuen 修改版!")
    server.logger.info("若需要原版，请在下面的网址下载（或者用MPM）")
    server.logger.info("https://www.mcdreforged.org/plugins/start_stop_helper_r")
    server.logger.info("或者用 MPM")

    register(server, command, '开关服助手')

    '''
    server.register_help_message(
        '!!server',
        {
            'en_us': 'Start and stop server helper',
            'zh_cn': '开关服助手'
        }
    )
    server.register_command(
        Literal('!!server').
            requires(lambda src: src.has_permission(permissions['help'])).
            runs(lambda src: src.reply(server.rtr('start_stop_helper_r.help'))
        ).
            then(
            Literal('start').
                requires(lambda src: src.has_permission(permissions['start'])).
                runs(lambda src: server.start())
        ).
            then(
            Literal('stop').
                requires(lambda src: src.has_permission(permissions['stop'])).
                runs(lambda src: stop_server())
        ).
            then(
            Literal('stop_exit').
                requires(
                lambda src: src.has_permission(permissions['stop_exit'])).
                runs(lambda src: stop_exit_server())
        ).
            then(
            Literal('restart').
                requires(
                lambda src: src.has_permission(permissions['restart'])).
                runs(lambda src: server.restart())
        ).
            then(
            Literal('exit').
                requires(lambda src: src.has_permission(permissions['exit'])).
                runs(lambda src: server.exit())
        ).
            then(
            Literal('kill').
                requires(lambda src: src.has_permission(permissions['kill'])).
                runs(lambda src: server.kill())
        )
    )
    '''
