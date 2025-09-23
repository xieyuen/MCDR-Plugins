import re

from mcdreforged import Info, PluginServerInterface
from mcdreforged.handler.impl import VanillaHandler


class DevelopHandler(VanillaHandler):
    def get_name(self) -> str:
        return "develop_handler"

    def parse_server_stdout(self, text: str) -> Info:
        # 简单粗暴
        # 但是会导致终端和文件不相同
        # 待优化
        text = re.sub(r'\[Not Secure] \[([^]]+)]', r'<\1>', text)

        return super().parse_server_stdout(text)


def on_load(server: PluginServerInterface, _old):
    server.register_server_handler(DevelopHandler())
