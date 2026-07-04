from typing import TYPE_CHECKING

from mcdreforged import PlayerCommandSource

from mcdrpost import constants
from mcdrpost.data_structure import Item, OrderInfo
from mcdrpost.utils import get_formatted_time
from mcdrpost.utils.translation import TranslationKeys

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class PostService:
    def __init__(self, mcdrpost: "MCDRpostMain"):
        self.mcdrpost = mcdrpost
        self.server = self.mcdrpost.server
        self.logger = self.server.logger

    @property
    def config(self):
        return self.mcdrpost.config_service.config

    @property
    def data_service(self):
        return self.mcdrpost.data_service

    @property
    def mcva_service(self):
        return self.mcdrpost.mcva_service

    # 音效播放
    def _play_sound(self, player: str, sound: str) -> None:
        """播放音效

        Args:
            player (str): 玩家名
            sound (str): 音效名
        """
        self.server.execute(
            constants.Commands.PLAY_SOUND_NEW.format(player, sound)
        )

    def _play_successfully_post_sound(self, sender: str, receiver: str) -> None:
        """播放发送成功音效"""
        self._play_sound(sender, constants.Sounds.SUCCESSFULLY_POST_SENDER)
        self._play_sound(receiver, constants.Sounds.SUCCESSFULLY_POST_RECEIVER)

    def _play_successfully_receive_sound(self, player: str) -> None:
        """播放接收成功音效"""
        self._play_sound(player, constants.Sounds.SUCCESSFULLY_RECEIVE)

    def play_has_something_to_receive_sound(self, player: str) -> None:
        """播放有新邮件音效"""
        self._play_sound(player, constants.Sounds.HAS_SOMETHING_TO_RECEIVE)

    # 辅助方法
    def get_offhand_item(self, player: str) -> Item | None:
        """获取玩家副手物品

        Args:
            player (str): 玩家 ID

        Returns:
            Item | None: 物品信息，副手为空时返回 None
        """
        try:
            item = self.mcva_service.get_offhand_item(player)
        except Exception:
            return None
        if not item or item.id == "minecraft:air":
            return None
        return item

    def check_offhand_empty(self, player: str) -> bool:
        """检查副手是否为空

        Args:
            player (str): 玩家 ID

        Returns:
            bool: 副手是否为空
        """
        return self.get_offhand_item(player) is None

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID

        Returns:
            bool: 是否达到上限
        """
        if self.config.max_storage == -1:
            return False
        return (
            len(self.data_service.get_orderid_by_sender(player))
            >= self.config.max_storage
        )

    # 核心功能
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

        # 检查存储上限
        if self.is_storage_full(sender):
            src.reply(
                TranslationKeys.post_fail_reached_max_storage.rtr(
                    self.config.max_storage
                )
            )
            return

        # 检查是否发给自己
        if sender == receiver:
            src.reply(TranslationKeys.post_fail_send_to_self.rtr())
            return

        # 检查收件人是否注册
        if not self.data_service.is_player_registered(receiver):
            src.reply(TranslationKeys.post_fail_receiver_unregistered.rtr())
            return

        # 默认备注
        if comment is None:
            comment = TranslationKeys.post_default_comment.tr()

        # 获取副手物品
        item = self.get_offhand_item(sender)
        if item is None:
            src.reply(TranslationKeys.post_fail_invalid_item.rtr())
            return

        # 创建订单
        order_id = self.data_service.create_order(
            OrderInfo(
                sender=sender,
                receiver=receiver,
                item=item,
                comment=comment,
                time=get_formatted_time(),
            )
        )

        # 清空副手
        self.mcva_service.replace(sender, constants.AIR)

        # 发送成功消息
        src.reply(TranslationKeys.post_success_sender.rtr())
        self.server.tell(receiver, TranslationKeys.post_success_receiver.rtr(order_id))

        # 播放音效
        self._play_successfully_post_sound(sender, receiver)

        # 保存数据
        self.data_service.save()

    def receive(
        self, src: PlayerCommandSource, order_id: int
    ) -> bool:
        """接收订单的物品

        Args:
            src (PlayerCommandSource): 命令源
            order_id (int): 被接收的订单的 ID

        Returns:
            bool: 是否成功接收到物品
        """
        player = src.player

        # 副手有东西，拒绝接收
        if not self.check_offhand_empty(player):
            src.reply(TranslationKeys.receive_fail_hands_not_cleared.rtr())
            return False

        # 检查订单是否存在
        if not self.data_service.contain_order(order_id):
            src.reply(TranslationKeys.receive_fail_undefined_id.rtr())
            return False

        # 检查权限
        if order_id not in self.data_service.get_orderid_by_receiver(player):
            src.reply(TranslationKeys.receive_fail_no_right.rtr())
            return False

        # 弹出订单
        order = self.data_service.pop_order(order_id)

        # 给予物品
        self.mcva_service.replace(player, order.item)

        # 播放音效
        self._play_successfully_receive_sound(player)

        # 保存数据
        self.data_service.save()

        return True

    def cancel(
        self, src: PlayerCommandSource, order_id: int
    ) -> bool:
        """取消订单

        Args:
            src (PlayerCommandSource): 命令源
            order_id (int): 被取消的订单的 ID

        Returns:
            bool: 是否成功取消
        """
        player = src.player

        # 副手有东西，拒绝取消（因为要把物品还给发件人）
        if not self.check_offhand_empty(player):
            src.reply(TranslationKeys.cancel_fail_hands_not_cleared.rtr())
            return False

        # 检查订单是否存在
        if not self.data_service.contain_order(order_id):
            src.reply(TranslationKeys.cancel_fail_undefined_id.rtr())
            return False

        # 检查权限
        if order_id not in self.data_service.get_orderid_by_sender(player):
            src.reply(TranslationKeys.cancel_fail_no_right.rtr())
            return False

        # 弹出订单
        order = self.data_service.pop_order(order_id)

        # 把物品还给发件人
        self.mcva_service.replace(player, order.item)

        # 保存数据
        self.data_service.save()

        return True
