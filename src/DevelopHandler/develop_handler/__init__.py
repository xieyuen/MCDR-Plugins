import re

from mcdreforged import Info, Literal, PluginServerInterface
from mcdreforged.handler.impl import VanillaHandler


class DevelopHandler(VanillaHandler):
    def get_name(self) -> str:
        return "develop_handler"

    def parse_server_stdout(self, text: str) -> Info:
        text = re.sub(r'\[Not Secure] \[([^]]+)]', r'<\1>', text)

        return super().parse_server_stdout(text)


def on_load(server: PluginServerInterface, _old):
    server.register_server_handler(DevelopHandler())
    server.register_command(
        Literal('!!test')
        .runs(lambda: server.execute('execute as test run say event.test'))
    )
