from collections import defaultdict
from typing import DefaultDict, Literal, overload

from mcdreforged import PluginServerInterface

from mcdrpost.config import Configuration
from mcdrpost.core.managers.data_manager import DataManager
from mcdrpost.core.services.config_service import ConfigService
from mcdrpost.data_structure import Order, OrderData, OrderInfo
from mcdrpost.utils.translation import TranslationKeys


class DataIndex:
    """数据索引

    Attributes:
        receiver (DefaultDict[str, list[int]]):
            收件人索引, key 为收件人名单, value 是对应的订单 ID
        sender (DefaultDict[str, list[int]]):
            发件人索引, key 为发件人名单, value 是对应的订单 ID
    """

    def __init__(self) -> None:
        self.receiver: DefaultDict[str, list[int]] = defaultdict(list)
        self.sender: DefaultDict[str, list[int]] = defaultdict(list)
        self.all: list[int] = []

    def __clear(self) -> None:
        """清除索引"""
        self.receiver.clear()
        self.sender.clear()
        self.all.clear()

    def build(self, data: OrderData) -> None:
        """(重新)构建索引, 只用于重载数据时"""
        self.__clear()

        for order in data.orders.values():
            self.add(order)

    def add(self, order: Order) -> None:
        """添加索引, 只应在新增订单或重新构建索引时调用"""
        self.receiver[order.receiver].append(order.id)
        self.receiver[order.receiver].sort()
        self.sender[order.sender].append(order.id)
        self.sender[order.sender].sort()
        self.all.append(order.id)

    def remove(self, order: Order) -> None:
        """删除索引"""
        self.receiver[order.receiver].remove(order.id)
        self.sender[order.sender].remove(order.id)
        self.all.remove(order.id)


class DataService:
    @property
    def config(self) -> Configuration:
        return self.config_service.config

    @property
    def data(self) -> OrderData:
        return self.data_manager.data

    def __init__(
            self, server: PluginServerInterface, config_service: ConfigService,
    ) -> None:
        server.logger.debug("Initializing DataService")
        self.server = server
        self.logger = server.logger
        self.data_manager = DataManager(server)
        self.config_service = config_service
        self.index = DataIndex()
        self.index.build(self.data)

    def __get_next_id(self) -> int:
        """获取最小的未使用 ID"""
        if not self.data.orders:
            return 1

        order_id = 1
        all_id = {int(i) for i in self.data.orders}

        while order_id in all_id:
            order_id += 1

        return order_id

    def create_order(self, info: OrderInfo) -> int:
        """创建订单并保存

        Args:
            info (OrderInfo): 订单信息

        Returns:
            int: 订单 ID
        """
        self.logger.debug("Creating new order")

        order_id = self.__get_next_id()

        order = Order(
            id=order_id,
            time=info.time,
            sender=info.sender,
            receiver=info.receiver,
            comment=info.comment,
            item=info.item,
        )
        self.data.orders[str(order_id)] = order
        self.index.add(order)

        self.logger.debug(f"New order created, id: {order_id}")
        return order_id

    def pop_order(self, order_id: int) -> Order:
        """弹出某订单"""
        self.logger.debug(f"Popping order with id: {order_id}")

        order = self.data.orders.pop(str(order_id))
        self.index.remove(order)

        return order

    def validate(self) -> None:
        policy = "fix" if self.config.auto_fix else "raise"

        for order_id, order in self.data.orders.items():
            if order_id == str(order.id):
                continue

            msg = TranslationKeys.data_validation_failed.rtr(order_id, order.id)
            if policy == "fix":
                self.server.logger.warning(msg)
                order.id = int(order_id)
            elif policy == "raise":
                raise ValueError(msg)
            else:
                assert False

    def reload(self) -> None:
        """重新加载数据"""
        self.data_manager.reload()
        self.validate()
        self.index.build(self.data)

    def save(self) -> None:
        """保存数据"""
        self.data_manager.save()

    @overload
    def has_order(self, order_id: int) -> bool:
        """检查是否存在某个订单"""

    @overload
    def has_order(self, order_id: int, player: str, typ: Literal["sender", "receiver"]) -> bool:
        """检查订单是否和某人有关（只检查收件人和发件人其中一种）"""

    def has_order(
            self,
            order_id: int,
            player: str | None = None,
            typ: Literal["sender", "receiver"] | None = None,
    ) -> bool:
        """检查订单的存在性

        支持两种调用方式：

        1) has_order(order_id: int) -> bool
           在全局订单索引中查找指定的 order_id。
        2) has_order(order_id: int, player: str, typ: Literal['sender','receiver']) -> bool
           在指定玩家的索引中查找 order_id。typ 为 'sender' 表示在发件人索引中查找，
           'receiver' 表示在收件人索引中查找。

        Args:
            order_id (int): 要检查的订单 ID。
            player (str, optional): 玩家名称；若为 None（默认）则进行全局查找。
            typ ({'sender', 'receiver'}, optional): 当提供 player 时必须指定，指示检查发件人或收件人索引。

        Returns:
            bool: 若找到返回 True，否则 False。

        Raises:
            AssertionError: 当 player 不为 None 且 typ 不合理时触发。

        Examples:
            >>> self.has_order(1)
            True
            >>> self.has_order(2, 'someone_who_has_no_order', 'receiver')
            False
        """
        if not player:
            return order_id in self.index.all
        if typ == "sender":
            return order_id in self.index.sender[player]
        elif typ == "receiver":
            return order_id in self.index.receiver[player]
        else:
            assert False, f"Unexpected type of player: {typ}"
