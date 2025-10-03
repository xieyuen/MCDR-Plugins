"""
邮件发送和接收服务
"""
from typing import TYPE_CHECKING

import time
from mcdreforged import InfoCommandSource, new_thread, PluginServerInterface, Info

import minecraft_data_api as api
from mcdrpost import constants
from mcdrpost.data_structure import OrderInfo, Item
from mcdrpost.utils import get_formatted_time
from mcdrpost.utils.exception import InvalidItem
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager


class PostService:
    """邮件发送和接收服务"""

    def __init__(self, post_manager: "PostManager") -> None:
        self._post_manager = post_manager
        self._server = post_manager.server
        self._data_manager = post_manager.data_manager
        self._config = post_manager.configuration
        self._version_manager = post_manager.version_manager

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID
        """
        if self._config.max_storage == -1:
            return False
        return len(self._data_manager.get_orderid_by_sender(player)) >= self._config.max_storage

    def check_offhand_empty(self, player: str) -> bool:
        """检查副手物品

        Args:
            player (str): 玩家 id
        """
        try:
            item = self.get_offhand_item(player)
        except InvalidItem:
            return True
        return item is None

    def get_offhand_item(self, player: str) -> Item | None:
        """获取玩家副手物品

        Args:
            player (str): 玩家 ID
        """
        item = self._version_manager.get_offhand_item(player)
        if not item:
            return None
        return item

    def replace(self, player: str, item: Item) -> None:
        """替换玩家的副手物品

        Args:
            player (str): 玩家 id
            item (Item): 要替换的物品
        """
        self._version_manager.replace(player, item)

    def post(self, src: InfoCommandSource, receiver: str, comment: str | None = None) -> None:
        """发送订单

        Args:
            src (InfoCommandSource): 寄件人的相关信息
            receiver (str): 收件人 ID
            comment (str): 备注信息
        """
        sender = src.get_info().player

        if self.is_storage_full(sender):
            src.reply(TranslationKeys.at_max_storage.tr(self._config.max_storage))
            return

        if sender == receiver:
            src.reply(TranslationKeys.same_person.tr())
            return

        if comment is None:
            comment = TranslationKeys.no_comment.tr()

        try:
            item = self.get_offhand_item(sender)
        except InvalidItem:
            src.reply(TranslationKeys.check_offhand.tr())
            return
        except:
            src.reply(TranslationKeys.error.running.tr())
            raise

        if item is None:
            src.reply(TranslationKeys.check_offhand.tr())
            return

        # create order
        order_id = self._data_manager.add_order(OrderInfo(
            sender=sender,
            receiver=receiver,
            item=item,
            comment=comment,
            time=get_formatted_time(),
        ))

        self.replace(sender, constants.AIR)
        src.reply(TranslationKeys.reply_success_post.tr())
        self._server.tell(receiver, TranslationKeys.hint_receive.tr(order_id))
        self._version_manager.play_sound.successfully_post(sender, receiver)
        self._data_manager.save()

    def receive(self, src: InfoCommandSource, order_id: int, typ: str) -> bool:
        """接收订单的物品

        Args:
            src (InfoCommandSource): 命令源
            order_id (int): 被接收的订单的 ID
            typ (str): 类型

        Returns:
            bool: 是否成功接收到物品
        """
        player = src.get_info().player

        # 副手有东西 拒绝接收
        if not self.check_offhand_empty(player):
            src.reply(TranslationKeys.clear_offhand.tr())
            return False

        # 不是 TA
        if typ == 'receive' and order_id not in self._data_manager.get_orderid_by_receiver(player):
            src.reply(TranslationKeys.unchecked_orderid.tr())
            return False
        elif typ == 'cancel' and order_id not in self._data_manager.get_orderid_by_sender(player):
            src.reply(TranslationKeys.unchecked_orderid.tr())
            return False

        order = self._data_manager.pop_order(order_id)
        self.replace(player, order.item)
        self._version_manager.play_sound.successfully_receive(player)
        return True

    def on_player_joined(self, server: PluginServerInterface, player: str, _info: Info) -> None:
        """事件: 玩家加入服务器"""
        if not self._data_manager.is_player_registered(player):
            if self._config.auto_register:
                # 还未注册的玩家
                self._data_manager.add_player(player)
                server.logger.info(TranslationKeys.login_log.tr(player))
                self._data_manager.save()
                return

            # 通知权限在admin以上的管理员有新玩家加入
            player_list = api.get_server_player_list()[-1]
            for online_player in player_list:
                if server.get_permission_level(online_player) >= 3:
                    server.tell(online_player, TranslationKeys.new_player_joined.tr(player))
            server.logger.info(TranslationKeys.new_player_joined.tr(player))
            return

        # 已注册的玩家，向他推送订单消息（如果有）
        if self._data_manager.has_unreceived_order(player):
            @new_thread('MCDRpost | send receive tip')
            def send_receive_tip():
                time.sleep(self._config.receive_tip_delay)
                server.tell(player, TranslationKeys.wait_for_receive.tr())
                self._version_manager.play_sound.has_something_to_receive(player)

            send_receive_tip()