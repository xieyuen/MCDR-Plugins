import enum
from typing import TYPE_CHECKING

from mcdreforged import new_thread

from mcdrpost import constants
from mcdrpost.config import Configuration
from mcdrpost.constants import Commands
from mcdrpost.data_structure import OrderInfo
from mcdrpost.utils import get_formatted_time

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class ReceivingStatsCode(enum.IntEnum):
    success = enum.auto()
    order_unexisted = enum.auto()
    order_belongs_to_other = enum.auto()
    offhand_not_empty = enum.auto()


class PostingFailureCode(enum.IntEnum):
    invalid_item = enum.auto()
    reached_max_storage = enum.auto()
    send_to_self = enum.auto()
    receiver_unregistered = enum.auto()


class PostService:
    @property
    def config(self) -> Configuration:
        return self.mp.config_service.config

    def __init__(self, mcdrpost: "MCDRpostMain"):
        mcdrpost.logger.info("Initializing PostService")
        self.mp = mcdrpost
        self.server = self.mp.server
        self.logger = self.server.logger

    def play(self, player: str, sound: str) -> None:
        self.server.execute(Commands.PLAY_SOUND.format(player, sound))

    @new_thread("MCDRpost PostService: send")
    def send(self, sender: str, receiver: str, comment: str | None = None) -> int | PostingFailureCode:
        """发送订单

        Args:
            sender (str):  发件人
            receiver (str): 收件人
            comment (str, optional): 备注

        Returns:
            int | PostingFailureCode: 订单号或失败代码
        """
        self.logger.info(f"player {sender} wants to send item to {receiver}")

        if sender == receiver:
            return PostingFailureCode.send_to_self
        if not self.mp.data_service.has_player(receiver):
            return PostingFailureCode.receiver_unregistered
        if 0 < self.config.max_storage <= self.mp.data_service.number_of_sent_orders(sender):
            return PostingFailureCode.reached_max_storage

        item = self.mp.mcva_service.get_offhand_item(sender)

        if not item:
            return PostingFailureCode.invalid_item

        self.logger.info(f"detected item from {sender}: {item}")
        self.logger.info(f"posting...")

        self.mp.mcva_service.replace(sender, constants.AIR)

        info = OrderInfo(
            time=get_formatted_time(),
            sender=sender,
            receiver=receiver,
            item=item,
            comment=comment,
        )
        id = self.mp.data_service.create_order(info)

        self.play(sender, self.config.sound.successfully_post_sender)
        self.play(receiver, self.config.sound.successfully_post_receiver)

        return id

    @new_thread("MCDRpost PostService: receive")
    def receive(self, player: str, order_id: int) -> ReceivingStatsCode:
        """接受物品

        Args:
            player (str): 玩家
            order_id (int): 订单 ID

        Returns:
            ReceivingStatsCode: 状态码
        """
        self.logger.info(f"player {player} wants to receive order {order_id}")

        if not self.mp.data_service.has_order(order_id):
            self.logger.info(f"No order with id: {order_id}")
            return ReceivingStatsCode.order_unexisted
        elif not self.mp.data_service.has_order(order_id, player, "receiver"):
            self.logger.info(f"No order with id: {order_id} for {player}")
            return ReceivingStatsCode.order_belongs_to_other

        if self.mp.mcva_service.get_offhand_item(player):
            self.logger.info(f"{player} didn't empty offhand")
            return ReceivingStatsCode.offhand_not_empty

        order = self.mp.data_service.get_order(order_id)

        self.mp.mcva_service.replace(player, order.item)

        self.play(player, self.config.sound.successfully_receive)

        return ReceivingStatsCode.success

    @new_thread("MCDRpost PostService: cancel")
    def cancel(self, player: str, order_id: int) -> ReceivingStatsCode:
        """取消订单

        Args:
            player (str): 玩家
            order_id (int): 订单 ID

        Returns:
            ReceivingStatsCode: 状态码
        """
        self.logger.info(f"player {player} wants to cancel order {order_id}")

        if not self.mp.data_service.has_order(order_id):
            self.logger.info(f"No order with id: {order_id}")
            return ReceivingStatsCode.order_unexisted
        elif not self.mp.data_service.has_order(order_id, player, "receiver"):
            self.logger.info(f"No order with id: {order_id} for {player}")
            return ReceivingStatsCode.order_belongs_to_other

        if self.mp.mcva_service.get_offhand_item(player):
            self.logger.info(f"{player} didn't empty offhand")
            return ReceivingStatsCode.offhand_not_empty

        order = self.mp.data_service.get_order(order_id)

        self.mp.mcva_service.replace(player, order.item)

        self.play(player, self.config.sound.successfully_receive)

        return ReceivingStatsCode.success
