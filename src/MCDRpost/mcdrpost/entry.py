"""
插件的入口文件

这里插件会把需要的事件传给各个服务处理
"""

import time

from mcdreforged import Info, PluginServerInterface, new_thread

from mcdrpost.core.main import MCDRpostMain
from mcdrpost.utils.translation import TranslationKeys

mcdrpost: MCDRpostMain | None = None


def on_load(server: PluginServerInterface, prev_module):
    """插件加载事件"""
    global mcdrpost
    mcdrpost = MCDRpostMain(server)

    # 重载配置和数据
    mcdrpost.config_service.reload()
    mcdrpost.data_service.reload()

    # 注册命令
    mcdrpost.command_manager.register()

    # 如果服务器已经在运行（热重载），触发服务器启动事件
    if server.is_server_running():
        on_server_startup(server)


def on_unload(server: PluginServerInterface):
    """插件卸载事件"""
    if mcdrpost is not None:
        mcdrpost.data_service.save()


def on_server_startup(server: PluginServerInterface):
    """服务器启动事件"""
    if mcdrpost is not None:
        mcdrpost.mcva_service.refresh()


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    """服务器停止事件"""
    if mcdrpost is not None:
        mcdrpost.data_service.save()


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    """玩家加入服务器事件"""
    if mcdrpost is None:
        return

    data_service = mcdrpost.data_service
    config = mcdrpost.config_service.config
    post_service = mcdrpost.post_service

    # 检查玩家是否已注册
    if not data_service.is_player_registered(player):
        if config.auto_register:
            # 自动注册新玩家
            data_service.add_player(player)
            server.logger.info(TranslationKeys.data_auto_register.rtr(player))
            data_service.save()
            return

        # 通知管理员有新玩家加入
        try:
            import minecraft_data_api as api

            player_list = api.get_server_player_list()[-1]
            for online_player in player_list:
                if server.get_permission_level(online_player) >= 3:
                    server.tell(
                        online_player,
                        TranslationKeys.on_new_player_joined.rtr(player),
                    )
        except ImportError:
            pass

        server.logger.info(TranslationKeys.on_new_player_joined.rtr(player))
        return

    # 已注册的玩家，检查是否有未接收的邮件
    if data_service.has_unreceived_order(player):

        @new_thread("MCDRpost|send receiving tip")
        def send_receive_tip():
            time.sleep(config.receiving_tip_delay)
            server.tell(player, TranslationKeys.on_old_player_joined.rtr())
            post_service.play_has_something_to_receive_sound(player)

        send_receive_tip()
