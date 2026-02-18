import re
import time
from typing import Any

from dowhen import when
from dowhen.handler import EventHandler
from mcdreforged import *


class Config(Serializable):
    waiting_time: float = 60
    """等待时间, 超时之后才强制关闭服务器, 单位为秒"""

    def validate_attribute(self, attr_name: str, attr_value: Any, **kwargs):
        if attr_value <= 0:
            raise ValueError(f"配置项 waiting_time 必须是正值, 实际配置: {attr_value}")
        if attr_value <= 3:
            server_interface.logger.warning(f"配置项 waiting_time 单位为秒, 实际配置 {attr_value} 可能过小")


server_interface: PluginServerInterface
config: Config

handler: EventHandler
is_world_saved: bool = False


def force_kill_server():
    """强制关闭服务器"""

    @new_thread("KillServer")
    def logic():
        """开新线程运行并且保证 force_kill_server 返回 None"""
        server_interface.logger.info("检测到服务器关闭命令执行, 等待服务器自动关闭")

        time.sleep(config.waiting_time)
        if not server_interface.is_server_running():
            return
        server_interface.logger.info("等待服务器关闭超时, 正在强制关闭服务器")
        # TODO: 检查世界是否保存
        # if not is_world_saved:
        #     server_interface.logger.warning("世界未完全保存, 重新等待")
        #     goto("time.sleep(config.waiting_time)")
        #     return
        server_interface.kill()

    logic()


def on_load(server: PluginServerInterface, prev_module):
    global server_interface, config, handler
    server_interface = server
    config = server.load_config_simple(target_class=Config)

    if prev_module is not None:
        prev_module.handler.remove()

    handler = when(server.stop, "return").do(force_kill_server)


def on_server_startup(_server: PluginServerInterface):
    global is_world_saved
    is_world_saved = False


def on_info(_server: PluginServerInterface, info: Info):
    if re.fullmatch(r".*All dimensions are saved", info.content):
        global is_world_saved
        is_world_saved = True
