import re
import time

from dowhen import when
from dowhen.handler import EventHandler
from mcdreforged import Info, PluginEvent, PluginServerInterface, event_listener, new_thread

from kill_server.config import Config
from kill_server.events import PluginStoppingServerEvent, ServerStoppingEvent, WorldSavedEvent

PAUSE_PROMPT: tuple[str, str] = ("请按任意键继续. . . ", "Press any key to continue . . . ")

psi: PluginServerInterface
config: Config
handler: EventHandler

is_world_saved: bool = False


def on_server_startup(_server: PluginServerInterface):
    global is_world_saved
    is_world_saved = False


@event_listener(WorldSavedEvent)
def on_world_saved(_server: PluginServerInterface):
    global is_world_saved
    is_world_saved = True


@new_thread("KillServer")
def force_kill_server(server: PluginServerInterface):
    """强制关闭服务器"""
    server.logger.info("检测到服务器关闭命令执行, 等待服务器自动关闭")

    time.sleep(config.waiting_time)
    if not server.is_server_running():
        server.logger.info("服务器已关闭, 取消强制关闭任务")
        return
    server.logger.info("等待服务器关闭超时, 正在强制关闭服务器")
    # TODO: 检查世界是否保存
    if not is_world_saved:
        server.logger.warning("世界仍未保存完成, 建议增加等待时间")
    server.kill()
    # kill 之后由 on_server_startup 把 is_world_saved 设置为 False


def dispatch(event: PluginEvent):
    psi.dispatch_event(event, ())


def on_load(server: PluginServerInterface, _prev_module):
    global psi, config, handler
    psi = server
    config = server.load_config_simple(target_class=Config)

    # noinspection PyTypeChecker
    handler = when(server.stop, "return").do(lambda: dispatch(PluginStoppingServerEvent))

    if not config.enable:
        server.logger.info("强制关闭功能已关闭")
        return
    if "just_kill_it" in server.get_plugin_list():
        server.logger.error("本插件与 Just Kill It 不兼容, enable 配置已设为 False")
        config.enable = False
        server.save_config_simple(config)
        # 后面不为事件注册监听器
    elif config.mcdr_only:
        server.logger.info("配置 mcdr_only 已启用")
        server.register_event_listener(PluginStoppingServerEvent, force_kill_server)
    else:
        server.register_event_listener(ServerStoppingEvent, force_kill_server)


def on_unload(_server: PluginServerInterface):
    handler.remove()


def on_info(server: PluginServerInterface, info: Info):
    if info.is_user:
        # 防熊
        return

    if re.fullmatch(r"Stopping the server", info.content):
        dispatch(ServerStoppingEvent)
        return
    if re.fullmatch(r".*All dimensions are saved", info.content):
        dispatch(WorldSavedEvent)
        return
    if info.raw_content in PAUSE_PROMPT:
        msgs = [
            "检测到 pause 命令的输出",
            "请检查 MCDR 配置文件内的 start_command 配置项和 MC 服务器启动脚本(如果存在)内有没有 pause 命令",
            "如果存在, 请尽快删除",
            "pause 引起的一些 issue:",
            "https://github.com/MCDReforged/MCDReforged/issues/394",
            "https://github.com/TISUnion/PrimeBackup/issues/85",
        ]
        for msg in msgs:
            server.logger.critical(msg)
        return
