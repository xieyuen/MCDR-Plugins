from collections import defaultdict
from typing import DefaultDict, Literal

from mcdreforged import PluginServerInterface

from mcdrpost.config import Configuration
from mcdrpost.core.managers.data_manager import DataManager
from mcdrpost.core.services.config_service import ConfigService
from mcdrpost.data_structure import Order, OrderData, OrderInfo
from mcdrpost.utils.translation import TranslationKeys


class DataValidator:
    @property
    def config(self) -> Configuration:
        return self.config_service.config

    def __init__(
        self, server: PluginServerInterface, config_service: ConfigService
    ) -> None:
        self.server = server
        self.config_service = config_service

    def validate(self, data: OrderData, *, policy: Literal["fix", "raise"]) -> None:
        orders = data.orders

        for order_id, order in orders.items():
            if order_id == str(order.id):
                continue

            msg = TranslationKeys.data_validation_failed.rtr(order_id, order.id)
            if policy == "fix":
                self.server.logger.warning(msg)
                order.id = int(order_id)
            elif policy == "raise":
                raise ValueError(msg)


class DataIndex:
    """数据索引

    Attributes:
        receiver_index (DefaultDict[str, list[int]]):
            收件人索引, key 为收件人名单, value 是对应的订单 ID
        sender_index (DefaultDict[str, list[int]]):
            发件人索引, key 为发件人名单, value 是对应的订单 ID
    """

    @property
    def data(self) -> OrderData:
        return self.data_service.data

    def __init__(self, data_service: "DataService") -> None:
        self.data_service = data_service
        self.receiver_index: DefaultDict[str, list[int]] = defaultdict(list)
        self.sender_index: DefaultDict[str, list[int]] = defaultdict(list)
        self.build()

    def __clear(self) -> None:
        """清除索引"""
        self.receiver_index.clear()
        self.sender_index.clear()

    def build(self) -> None:
        """只用于重载数据时"""
        self.__clear()

        for order in self.data.orders.values():
            self.add(order)

    def add(self, order: Order) -> None:
        """只应在新增订单或重新构建索引时调用"""
        self.receiver_index[order.receiver].append(order.id)
        self.receiver_index[order.receiver].sort()
        self.sender_index[order.sender].append(order.id)
        self.sender_index[order.sender].sort()

    def remove(self, order_id: int) -> None:
        order = self.data.orders[str(order_id)]
        self.receiver_index[order.receiver].remove(order_id)
        self.sender_index[order.sender].remove(order_id)


class DataService:
    @property
    def config(self) -> Configuration:
        return self.config_service.config

    @property
    def data(self) -> OrderData:
        return self.data_manager.data

    def __init__(
        self, server: PluginServerInterface, config_service: ConfigService
    ) -> None:
        self.server = server
        self.data_manager = DataManager(server)
        self.config_service = config_service
        self.validator = DataValidator(server, config_service)
        self.index = DataIndex(self)

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
            info(OrderIndo): 订单信息

        Returns:
            int: 订单 ID
        """

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

        return order_id

    def pop_order(self, order_id: int) -> Order:
        """弹出某订单"""
        raise NotImplementedError

    def reload(self) -> None:
        self.data_manager.reload()
        self.validator.validate(
            self.data, policy="fix" if self.config.auto_fix else "raise"
        )

    def save(self) -> None:
        self.data_manager.save()
