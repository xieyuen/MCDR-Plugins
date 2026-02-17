from typing import Literal, TYPE_CHECKING

from mcdreforged import InfoCommandSource, PlayerCommandSource, PluginServerInterface

from mcdrpost import constants
from mcdrpost.configuration import Configuration
from mcdrpost.data_structure import Item, OrderInfo
from mcdrpost.utils.exception import InvalidItem
from mcdrpost.utils.general import get_formatted_time
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.coordinator import MCDRpostCoordinator


class PostManager:
    """插件核心功能处理"""

    def __init__(self, coo: "MCDRpostCoordinator") -> None:
        self.coordinator = coo
        self.server: PluginServerInterface = coo.server
        self.version_manager = coo.version_manager
        self.data_manager = coo.data_manager

    @property
    def config(self) -> Configuration:
        return self.coordinator.config

    # Helper methods
    def replace(self, player: str, item: Item) -> None:
        """替换玩家的副手物品

        Args:
            player (str): 玩家 id
            item (Item): 要替换的物品
        """
        self.version_manager.replace(player, item)

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
        item = self.version_manager.get_offhand_item(player)
        if not item:
            return None
        return item

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID
        """
        if self.config.max_storage == -1:
            return False
        return (
                len(self.data_manager.get_orderid_by_sender(player))
                >= self.config.max_storage
        )

    def post(
            self, src: PlayerCommandSource, receiver: str, comment: str | None = None
    ) -> None:
        """发送订单

        Args:
            src (PlayerCommandSource): 寄件人的相关信息
            receiver (str): 收件人 ID
            comment (str): 备注信息
        """
        sender = src.player

        if self.is_storage_full(sender):
            src.reply(TranslationKeys.post_fail_reached_max_storage.rtr(self.config.max_storage))
            return

        if sender == receiver:
            src.reply(TranslationKeys.post_fail_send_to_self.rtr())
            return

        if comment is None:
            comment = TranslationKeys.post_default_comment.tr()

        try:
            item = self.get_offhand_item(sender)
        except InvalidItem:
            src.reply(TranslationKeys.post_fail_invalid_item.rtr())
            return
        except Exception:
            src.reply(TranslationKeys.error_occurred.rtr())
            raise

        if item is None:
            src.reply(TranslationKeys.post_fail_invalid_item.rtr())
            return

        # create order
        order_id = self.data_manager.add_order(
            OrderInfo(
                sender=sender,
                receiver=receiver,
                item=item,
                comment=comment,
                time=get_formatted_time(),
            )
        )

        self.replace(sender, constants.AIR)
        src.reply(TranslationKeys.post_success_sender.rtr())
        self.server.tell(receiver, TranslationKeys.post_success_receiver.rtr(order_id))
        self.version_manager.play_sound.successfully_post(sender, receiver)
        self.data_manager.save()

    def receive(
            self, src: PlayerCommandSource, order_id: int, typ: Literal["cancel", "receive"]
    ) -> bool:
        """接收订单的物品

        Args:
            src (InfoCommandSource): 命令源
            order_id (int): 被接收的订单的 ID
            typ (Literal["cancel", "receive"]): 类型

        Returns:
            bool: 是否成功接收到物品
        """
        player = src.player

        # 副手有东西 拒绝接收
        if not self.check_offhand_empty(player):
            src.reply(TranslationKeys.receive_fail_hands_not_cleared.rtr())
            return False

        if not self.data_manager.contain_order(order_id):
            src.reply(TranslationKeys.receive_fail_undefined_id.rtr())
            return False

        # 不是 TA
        if (
                typ == "receive"
                and order_id not in self.data_manager.get_orderid_by_receiver(player)
        ):
            src.reply(TranslationKeys.receive_fail_no_right.rtr())
            return False
        elif (
                typ == "cancel"
                and order_id not in self.data_manager.get_orderid_by_sender(player)
        ):
            src.reply(TranslationKeys.cancel_fail_no_right.rtr())
            return False

        order = self.data_manager.pop_order(order_id)
        self.replace(player, order.item)
        self.version_manager.play_sound.successfully_receive(player)
        return True
