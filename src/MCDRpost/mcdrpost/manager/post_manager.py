import time
from typing import Literal

from mcdreforged import Info, InfoCommandSource, PluginServerInterface, new_thread

import minecraft_data_api as api
from mcdrpost import constants
from mcdrpost.configuration import Configuration
from mcdrpost.data_structure import Item, OrderInfo
from mcdrpost.manager.command_manager import CommandManager
from mcdrpost.manager.config_manager import ConfigurationManager
from mcdrpost.manager.data_manager import DataManager
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.utils import get_formatted_time, play_sound
from mcdrpost.utils.exception import InvalidItem
from mcdrpost.utils.translation import Tags, tr


class PostManager:
    """Post 管理器，也是插件核心逻辑处理的地方

    Attributes:
        server (PluginServerInterface): MCDR插件接口
        config_manager (ConfigurationManager): 配置管理
        data_manager (DataManager): 订单管理
        command_manager (CommandManager): 命令注册
    """

    def __init__(self, server: PluginServerInterface) -> None:
        self.server: PluginServerInterface = server
        self.config_manager: ConfigurationManager = ConfigurationManager(self)
        self.data_manager: DataManager = DataManager(self)
        self.command_manager: CommandManager = CommandManager(self)
        self.version_manager: VersionManager = VersionManager(self.server)

    @property
    def configuration(self) -> Configuration:
        return self.config_manager.get_configuration()

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
            if self.configuration.auto_register:
                # 还未注册的玩家
                self.data_manager.add_player(player)
                server.logger.info(tr(Tags.login_log, player))
                self.data_manager.save()
                return

            # 通知权限在admin以上的管理员有新玩家加入
            player_list = api.get_server_player_list()[-1]
            for online_player in player_list:
                if server.get_permission_level(online_player) >= 3:
                    server.tell(online_player, tr(Tags.new_player_joined, player))
            server.logger.info(tr(Tags.new_player_joined, player))
            return

        # 已注册的玩家，向他推送订单消息（如果有）
        if self.data_manager.has_unreceived_order(player):
            @new_thread('MCDRpost | send receive tip')
            def send_receive_tip():
                time.sleep(self.configuration.receive_tip_delay)
                server.tell(player, tr(Tags.wait_for_receive))
                play_sound.has_something_to_receive(server, player)

            send_receive_tip()

    def on_server_startup(self, _server: PluginServerInterface):
        """事件: 服务器完全开启--刷新游戏版本设置"""
        self.version_manager.refresh()

    def on_server_stop(self, _server: PluginServerInterface, _server_return_code: int):
        """事件: 服务器关闭--保存配置信息和订单信息"""
        self.data_manager.save()

    # Helper methods
    def replace(self, player: str, item: Item) -> None:
        """替换玩家的副手物品

        Args:
            player (str): 玩家 id
            item (Item): 要替换的物品
        """
        self.version_manager.replace(player, item)

    def get_offhand_item(self, player: str) -> Item:
        """获取玩家副手物品

        Args:
            player (str): 玩家 ID
        """
        item = self.version_manager.get_offhand_item(player)
        if not item:
            raise InvalidItem(item)
        return item

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID
        """
        if self.configuration.max_storage == -1:
            return False
        return len(self.data_manager.get_orderid_by_sender(player)) >= self.configuration.max_storage

    def post(self, src: InfoCommandSource, receiver: str, comment: str = None) -> None:
        """发送订单

        Args:
            src (InfoCommandSource): 寄件人的相关信息
            receiver (str): 收件人 ID
            comment (str): 备注信息
        """
        sender = src.get_info().player

        if self.is_storage_full(sender):
            src.reply(tr(Tags.at_max_storage, self.configuration.max_storage))
            return

        if sender == receiver:
            src.reply(tr(Tags.same_person))
            return

        if comment is None:
            comment = tr(Tags.no_comment)

        try:
            item = self.get_offhand_item(sender)
        except InvalidItem as e:
            self.server.logger.warning(e)
            src.reply(tr(Tags.check_offhand))
            return
        except Exception as e:
            self.server.logger.error(e)
            src.reply(tr(Tags.check_offhand))
            return

        # create order
        order_id = self.data_manager.add_order(OrderInfo(
            sender=sender,
            receiver=receiver,
            item=item,
            comment=comment,
            time=get_formatted_time(),
        ))

        self.replace(sender, constants.AIR)
        src.reply(tr(Tags.reply_success_post))
        self.server.tell(receiver, tr(Tags.hint_receive, order_id))
        play_sound.successfully_post(self.server, sender, receiver)
        self.data_manager.save()

    def receive(self, src: InfoCommandSource, order_id: int, typ: Literal["cancel", "receive"]) -> bool:
        """接收订单的物品

        Args:
            src (InfoCommandSource): 命令源
            order_id (int): 被接收的订单的 ID
            typ (Literal["cancel", "receive"]): 类型

        Returns:
            bool: 是否成功接收到物品
        """
        player = src.get_info().player

        # 副手有东西 拒绝接收
        try:
            self.get_offhand_item(player)
        except InvalidItem:
            pass
        else:
            src.reply(tr(Tags.clear_offhand))
            return False

        # 不是 TA
        if typ == 'receive' and order_id not in self.data_manager.get_orderid_by_receiver(player):
            src.reply(tr(Tags.unchecked_orderid))
            return False
        elif typ == 'cancel' and order_id not in self.data_manager.get_orderid_by_sender(player):
            src.reply(tr(Tags.unchecked_orderid))
            return False

        order = self.data_manager.pop_order(order_id)
        self.replace(player, order.item)
        play_sound.receive(self.server, player)
        return True

    def reload(self) -> None:
        self.config_manager.reload()
        self.data_manager.reload()


__all__ = ['PostManager']
