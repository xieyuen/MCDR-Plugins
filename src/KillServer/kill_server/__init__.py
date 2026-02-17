import time
from typing import Any

from dowhen import when
from dowhen.handler import EventHandler
from mcdreforged import PluginServerInterface, Serializable, new_thread


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

@new_thread("KillServer")
def force_kill_server():
    """强制关闭服务器"""
    server_interface.logger.info("检测到服务器关闭命令执行, 等待服务器自动关闭")

    time.sleep(config.waiting_time)
    if server_interface.is_server_running():
        server_interface.logger.info("等待服务器关闭超时, 正在强制关闭服务器")
        server_interface.kill()


def on_load(server: PluginServerInterface, prev_module):
    global server_interface, config, handler
    server_interface = server
    config = server.load_config_simple(target_class=Config)

    if prev_module is not None:
        prev_module.handler.remove()

    handler = when(server.stop, "return").do(force_kill_server)
