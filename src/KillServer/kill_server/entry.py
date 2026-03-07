import re
import time

import dowhen
from dowhen.handler import EventHandler
from mcdreforged import Info, PluginServerInterface, event_listener, new_thread, PluginEvent

from kill_server.config import Config
from kill_server.events.server_event import ServerEvents, dispatch
from kill_server.handler_storage import HandlerStorage

PAUSE_PROMPT: tuple[str, str] = ("请按任意键继续. . . ", "Press any key to continue . . . ")

config: Config
handler_storage: HandlerStorage = HandlerStorage()

is_world_saved: bool = False


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


def __check_environment(server: PluginServerInterface) -> bool:
    from mcdreforged.mcdr_config import MCDReforgedConfig

    mcdr_cfg = MCDReforgedConfig.deserialize(server.get_mcdr_config())
    INVALID_HANDLERS = {"bungeecord_handler", "waterfall_handler", "velocity_handler"}

    if mcdr_cfg.handler in INVALID_HANDLERS:
        server.logger.error("本插件不支持跳转服")
        return False
    if "just_kill_it" in server.get_plugin_list():
        server.logger.error("本插件与 Just Kill It 不兼容")
        return False
    return True


def __reg_dispatcher(server: PluginServerInterface):
    def gen_handler(func, e: PluginEvent) -> tuple[PluginEvent, EventHandler]:
        return e, dowhen.when(
            func,
            "<start>",
        ).do(lambda: dispatch(e))

    handlers: list[tuple[PluginEvent, EventHandler]] = [
        gen_handler(server.stop, ServerEvents.PLUGIN_STOPPING_SERVER),
        gen_handler(server.kill, ServerEvents.PLUGIN_KILLING_SERVER),
    ]

    for event, handler in handlers:
        handler_storage.register(event, handler)


def on_load(server: PluginServerInterface, _prev_module):
    global config
    config = server.load_config_simple(target_class=Config)

    __reg_dispatcher(server)

    if not config.enable:
        server.logger.info("强制关闭功能已关闭")
        return
    if not __check_environment(server):
        server.logger.error("本插件已自动禁用")
        config.enable = False
        server.save_config_simple(config)
        # 后面不为事件注册监听器
        return

    if config.mcdr_only:
        server.logger.info("配置 mcdr_only 已启用")
        server.register_event_listener(ServerEvents.PLUGIN_STOPPING_SERVER, force_kill_server)
    else:
        server.register_event_listener(ServerEvents.SERVER_STOPPING, force_kill_server)


def on_unload(_server: PluginServerInterface):
    handler_storage.remove()


def on_info(server: PluginServerInterface, info: Info):
    if info.is_user:
        # 防熊
        return

    if re.fullmatch(r"Stopping the server", info.content):
        dispatch(ServerEvents.SERVER_STOPPING)
        return
    if re.fullmatch(r".*All dimensions are saved", info.content):
        dispatch(ServerEvents.WORLD_SAVED)
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


def on_server_startup(server: PluginServerInterface):
    global is_world_saved
    server.logger.debug("检测到服务器已完全启动")
    is_world_saved = False


@event_listener(ServerEvents.WORLD_SAVED)
def on_world_saved(server: PluginServerInterface):
    global is_world_saved
    server.logger.debug("检测到世界保存完成")
    is_world_saved = True


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    global is_world_saved
    server.logger.debug(f"检测到服务器已关闭, 返回值: {server_return_code}")
    # 认定服务器被其他因素强制关闭时世界已保存
    is_world_saved = True
