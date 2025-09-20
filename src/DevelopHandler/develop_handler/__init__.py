import re

from mcdreforged import Info, Literal, PluginServerInterface, Serializable, new_thread
from mcdreforged.handler.impl import VanillaHandler

import minecraft_data_api as api


class DevelopHandler(VanillaHandler):
    def get_name(self) -> str:
        return "develop_handler"

    def parse_server_stdout(self, text: str) -> Info:
        text = re.sub(r'\[Not Secure] \[([^]]+)]', r'<\1>', text)

        return super().parse_server_stdout(text)


class Configuration(Serializable):
    test: bool = True
    test_player: str = 'Test'


config: Configuration
player_list: list[str]


def test(server: PluginServerInterface):
    server.register_command(
        Literal('!!test')
        .runs(lambda: server.execute(f'execute as {config.test_player} run say !!test2'))
    )
    server.register_command(
        Literal('!!test2')
        .runs(lambda src, ctx: server.logger.info(f'Event.test({src=}, {ctx=})'))
    )


def on_load(server: PluginServerInterface, _old):
    global config
    server.register_server_handler(DevelopHandler())

    config = server.load_config_simple(target_class=Configuration)

    if config.test:
        test(server)

    if server.is_server_running():
        on_server_startup(server)


@new_thread("DevelopHandler | Test")
def get_online_player():
    global player_list
    player_list = api.get_server_player_list().players


def on_server_startup(server: PluginServerInterface):
    get_online_player().join()

    if config.test_player not in player_list:
        server.execute(f'player {config.test_player} spawn')

    if config.test:
        server.execute('say !!test')
