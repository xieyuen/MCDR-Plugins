import time
from typing import TYPE_CHECKING

from mcdreforged import Info, PluginServerInterface, new_thread

import minecraft_data_api as api
from mcdrpost.configuration import Configuration
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.coordinator import MCDRpostCoordinator


class EventManager:
    """MCDR Event Handling"""
    def __init__(self, coo: "MCDRpostCoordinator"):
        self.coo = coo

        self.config_manager = coo.config_manager
        self.data_manager = coo.data_manager
        self.version_manager = coo.version_manager
        self.command_manager = coo.command_manager

    @property
    def config(self) -> Configuration:
        return self.coo.config

    # Events Handle
    def on_load(self, server: PluginServerInterface, _prev_module) -> None:
        """事件: 插件加载--在这里会注册插件的命令

        如果服务端已经运行（也就是重新加载插件的情况），会自动地引发服务端启动完成事件

        .. note::
            PostManager在插件导入时通过 ``PluginServerInterface.psi()`` 获取到
                PluginServerInterface 实例进行实例化，
                而非一般的在 on_load() 内得到 PluginServerInterface 实例再实例化
        """
        self.config_manager.reload()
        self.data_manager.reload()
        self.command_manager.register()
        if server.is_server_running():
            self.on_server_startup(server)

    def on_unload(self, _server: PluginServerInterface) -> None:
        """事件: 插件卸载--保存订单信息"""
        self.data_manager.save()

    def on_player_joined(self, server: PluginServerInterface, player: str, _info: Info) -> None:
        """事件: 玩家加入服务器"""
        if not self.data_manager.is_player_registered(player):
            if self.config.auto_register:
                # 还未注册的玩家
                self.data_manager.add_player(player)
                server.logger.info(TranslationKeys.login_log.tr(player))
                self.data_manager.save()
                return

            # 通知权限在admin以上的管理员有新玩家加入
            player_list = api.get_server_player_list()[-1]
            for online_player in player_list:
                if server.get_permission_level(online_player) >= 3:
                    server.tell(online_player, TranslationKeys.new_player_joined.tr(player))
            server.logger.info(TranslationKeys.new_player_joined.tr(player))
            return

        # 已注册的玩家，向他推送订单消息（如果有）
        if self.data_manager.has_unreceived_order(player):
            @new_thread('MCDRpost|send receiving tip')
            def send_receive_tip():
                time.sleep(self.config.receiving_tip_delay)
                server.tell(player, TranslationKeys.wait_for_receive.tr())
                self.version_manager.play_sound.has_something_to_receive(player)

            send_receive_tip()

    def on_server_startup(self, _server: PluginServerInterface):
        """事件: 服务器完全开启--刷新游戏版本设置"""
        self.version_manager.refresh()

    def on_server_stop(self, _server: PluginServerInterface, _server_return_code: int):
        """事件: 服务器关闭--保存配置信息和订单信息"""
        self.data_manager.save()
