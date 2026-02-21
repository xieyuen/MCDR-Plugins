import re
import time

from dowhen import when
from dowhen.handler import EventHandler
from mcdreforged import *

from kill_server.config import Config

psi: PluginServerInterface
config: Config
handler: EventHandler

ServerStoppingEvent = LiteralEvent("kill_server.server_stopping")
PluginStoppingServerEvent = LiteralEvent("kill_server.plugin_stopping_server")
WorldSavedEvent = LiteralEvent("kill_server.world_saved")


@event_listener(ServerStoppingEvent)
@new_thread("KillServer")
def force_kill_server():
    """强制关闭服务器"""
    if not config.enable:
        return

    psi.logger.info("检测到服务器关闭命令执行, 等待服务器自动关闭")

    time.sleep(config.waiting_time)
    if not psi.is_server_running():
        return
    psi.logger.info("等待服务器关闭超时, 正在强制关闭服务器")
    # TODO: 检查世界是否保存
    psi.kill()


def dispatch(event: PluginEvent):
    psi.dispatch_event(event, ())


def on_load(server: PluginServerInterface, prev_module):
    global psi, config, handler
    psi = server
    config = server.load_config_simple(target_class=Config)

    if prev_module is not None:
        prev_module.handler.remove()

    # noinspection PyTypeChecker
    handler = when(server.stop, "return").do(lambda: dispatch(PluginStoppingServerEvent))


def on_info(_server: PluginServerInterface, info: Info):
def on_info(server: PluginServerInterface, info: Info):
    if re.fullmatch(r"Stopping the server", info.content):
        dispatch(ServerStoppingEvent)
        return
    if re.fullmatch(r".*All dimensions are saved", info.content):
        dispatch(WorldSavedEvent)
        return
    if info.content == "请按任意键继续. . .":
        msgs = [
            "检测到 pause 命令的输出",
            "请检查 MCDR 配置文件内的 start_command 配置项和(如果存在)启动脚本内有没有 pause 命令",
            "如果存在, 请尽快删除",
            "相关 issue:",
            "https://github.com/MCDReforged/MCDReforged/issues/394",
            "https://github.com/TISUnion/PrimeBackup/issues/85",
        ]
        for msg in msgs:
            server.logger.critical(msg)
        return
