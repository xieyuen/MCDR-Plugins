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

    def __init__(self) -> None:
        self.receiver_index: DefaultDict[str, list[int]] = defaultdict(list)
        self.sender_index: DefaultDict[str, list[int]] = defaultdict(list)

    def __clear(self) -> None:
        """清除索引"""
        self.receiver_index.clear()
        self.sender_index.clear()

    def build(self, data: OrderData) -> None:
        """(重新)构建索引, 只用于重载数据时"""
        self.__clear()

        for order in data.orders.values():
            self.add(order)

    def add(self, order: Order) -> None:
        """添加索引, 只应在新增订单或重新构建索引时调用"""
        self.receiver_index[order.receiver].append(order.id)
        self.receiver_index[order.receiver].sort()
        self.sender_index[order.sender].append(order.id)
        self.sender_index[order.sender].sort()

    def remove(self, order: Order) -> None:
        """删除索引"""
        self.receiver_index[order.receiver].remove(order.id)
        self.sender_index[order.sender].remove(order.id)


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
        server.logger.debug("Initializing DataService")
        self.server = server
        self.data_manager = DataManager(server)
        self.config_service = config_service
        self.validator = DataValidator(server, config_service)
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
        order = self.data.orders.pop(str(order_id))
        self.index.remove(order)

        return order

    def reload(self) -> None:
        """重新加载数据"""
        self.data_manager.reload()
        self.validator.validate(
            self.data, policy="fix" if self.config.auto_fix else "raise"
        )
        self.index.build(self.data)

    def save(self) -> None:
        """保存数据"""
        self.data_manager.save()

    # 玩家管理方法
    def is_player_registered(self, player: str) -> bool:
        """检查玩家是否已注册

        Args:
            player (str): 玩家名称

        Returns:
            bool: 是否已注册
        """
        return player in self.data.players

    def add_player(self, player: str) -> bool:
        """添加玩家

        Args:
            player (str): 玩家名称

        Returns:
            bool: 是否成功添加
        """
        if self.is_player_registered(player):
            return False
        self.data.players.append(player)
        return True

    def remove_player(self, player: str) -> bool:
        """移除玩家

        Args:
            player (str): 玩家名称

        Returns:
            bool: 是否成功移除
        """
        if not self.is_player_registered(player):
            return False
        self.data.players.remove(player)
        return True

    def get_players(self) -> list[str]:
        """获取所有已注册玩家列表

        Returns:
            list[str]: 玩家列表
        """
        return self.data.players.copy()

    # 订单查询方法
    def contain_order(self, order_id: int) -> bool:
        """检查订单是否存在

        Args:
            order_id (int): 订单 ID

        Returns:
            bool: 是否存在
        """
        return str(order_id) in self.data.orders

    def get_order_by_id(self, order_id: int) -> Order | None:
        """根据 ID 获取订单

        Args:
            order_id (int): 订单 ID

        Returns:
            Order | None: 订单对象，不存在则返回 None
        """
        return self.data.orders.get(str(order_id))

    def get_orderid_by_sender(self, sender: str) -> list[int]:
        """获取发件人的所有订单 ID

        Args:
            sender (str): 发件人名称

        Returns:
            list[int]: 订单 ID 列表
        """
        return self.index.sender_index.get(sender, []).copy()

    def get_orderid_by_receiver(self, receiver: str) -> list[int]:
        """获取收件人的所有订单 ID

        Args:
            receiver (str): 收件人名称

        Returns:
            list[int]: 订单 ID 列表
        """
        return self.index.receiver_index.get(receiver, []).copy()

    def get_orders_by_sender(self, sender: str) -> list[Order]:
        """获取发件人的所有订单

        Args:
            sender (str): 发件人名称

        Returns:
            list[Order]: 订单列表
        """
        order_ids = self.get_orderid_by_sender(sender)
        return [self.data.orders[str(oid)] for oid in order_ids]

    def get_orders_by_receiver(self, receiver: str) -> list[Order]:
        """获取收件人的所有订单

        Args:
            receiver (str): 收件人名称

        Returns:
            list[Order]: 订单列表
        """
        order_ids = self.get_orderid_by_receiver(receiver)
        return [self.data.orders[str(oid)] for oid in order_ids]

    def get_all_orders(self) -> list[Order]:
        """获取所有订单

        Returns:
            list[Order]: 所有订单列表
        """
        return list(self.data.orders.values())

    def has_unreceived_order(self, player: str) -> bool:
        """检查玩家是否有未接收的订单

        Args:
            player (str): 玩家名称

        Returns:
            bool: 是否有未接收的订单
        """
        return len(self.index.receiver_index.get(player, [])) > 0
