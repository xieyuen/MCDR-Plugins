from collections import defaultdict
from typing import DefaultDict, TYPE_CHECKING

from mcdrpost import constants
from mcdrpost.order_data import Order, OrderData, OrderInfo, OrderInfoDict
from mcdrpost.utils import tr
from mcdrpost.utils.exception import InvalidOrder
from mcdrpost.utils.translation_tags import Tags

if TYPE_CHECKING:
    from mcdrpost.manager.post_manager import PostManager  # noqa


class OrderManager:
    """订单管理器"""

    def __init__(self, post_manager: "PostManager") -> None:
        """初始化

        Args:
            post_manager (PostManager): 主管理器
        """
        # initialize
        self._post_manager: "PostManager" = post_manager
        self._logger = post_manager.server.logger
        self._config = post_manager.config_manager.configuration

        # index
        self._sender_orders: DefaultDict[str, list[int]] = defaultdict(list)
        self._receiver_orders: DefaultDict[str, list[int]] = defaultdict(list)

        # load data
        self._order_data: OrderData | None = None
        self.reload()

    def _build_index(self) -> None:
        """构建索引"""
        self._sender_orders.clear()
        self._receiver_orders.clear()
        for order in self._order_data.orders.values():
            self._sender_orders[order.sender].append(order.id)
            self._receiver_orders[order.receiver].append(order.id)

    def _check_orders(self) -> None:
        """检查订单

        主要是订单的 ID 能不能对上索引

        .. versionchanged:: v3.1.1
            改用索引作为订单 ID
        """
        for order_id, order in self._order_data.orders.items():
            if str(order.id) == order_id:
                continue
            if not self._config.auto_fix:
                raise InvalidOrder(tr(Tags.error.invalid_order, order_id, order.id))
            self._logger.error(tr(Tags.error.invalid_order, order_id, order.id))
            self._logger.error(tr(Tags.auto_fix.invalid_order, order_id))
            self._order_data.orders[order_id].id = int(order_id)

    def reload(self) -> None:
        self._order_data = self._post_manager.server.load_config_simple(
            constants.ORDERS_DATA_FILE_NAME,
            target_class=OrderData,
            file_format=constants.ORDERS_DATA_FILE_TYPE
        )
        self._check_orders()
        self._build_index()

    def save(self) -> None:
        self._post_manager.server.save_config_simple(
            self._order_data,
            constants.ORDERS_DATA_FILE_NAME,
            file_format=constants.ORDERS_DATA_FILE_TYPE,
        )

    def is_player_registered(self, player: str) -> bool:
        """检查玩家是否已经注册

        Args:
            player (str): 玩家名称

        Returns:
            bool: 是否已经注册
        """
        return player in self._order_data.players

    def add_player(self, player: str) -> bool:
        if player in self._order_data.players:
            return False
        self._order_data.players.append(player)
        return True

    def remove_player(self, player: str) -> bool:
        if player not in self._order_data.players:
            return False
        self._order_data.players.remove(player)
        return True

    def get_players(self) -> list[str]:
        return self._order_data.players

    def get_next_id(self) -> int:
        """获取最小的有效 ID"""
        if not self._order_data.orders:
            return 1

        order_id = 1
        id_set = set(o.id for o in self._order_data.orders.values())
        while order_id in id_set:
            order_id += 1

        return order_id

    def add_order(self, order: OrderInfo | OrderInfoDict) -> int:
        """添加订单

        Args:
            order (OrderInfo | OrderInfoDict): 订单信息

        Returns:
            int: 订单 ID

        Raises:
            TypeError: 订单信息类型错误（检查传入的数据类型是否为 ``dict`` 或者 ``OrderInfo``）
        """
        if isinstance(order, dict):
            order = OrderInfo.deserialize(order)
        elif not isinstance(order, OrderInfo):
            raise TypeError("不支持非 OrderInfo 类型的订单信息")

        order_id = self.get_next_id()
        self._order_data.orders[str(order_id)] = Order.deserialize(
            order.serialize(),
            id=order_id,
        )
        self._sender_orders[order.sender].append(order_id)
        self._receiver_orders[order.receiver].append(order_id)
        return order_id

    def remove_order(self, order_id: int) -> bool:
        if order_id not in self._order_data.orders:
            return False
        order = self._order_data.orders[str(order_id)]
        self._sender_orders[order.sender].remove(order_id)
        self._receiver_orders[order.receiver].remove(order_id)
        del self._order_data.orders[str(order_id)]
        return True

    def get_order(self, order_id: int) -> Order:
        return self._order_data.orders[str(order_id)]

    def get_orders(self) -> list[Order]:
        return list(self._order_data.orders.values())

    def get_orderid_by_sender(self, sender: str) -> list[int]:
        return self._sender_orders[sender]

    def get_orderid_by_receiver(self, receiver: str) -> list[int]:
        return self._receiver_orders[receiver]

    def get_orders_by_sender(self, sender: str) -> list[Order]:
        return [
            self._order_data.orders[str(order_id)]
            for order_id in self._sender_orders[sender]
        ]

    def get_orders_by_receiver(self, receiver: str) -> list[Order]:
        return [
            self._order_data.orders[str(order_id)]
            for order_id in self._receiver_orders[receiver]
        ]

    def has_unreceived_order(self, player: str) -> bool:
        return bool(self._receiver_orders[player])

    def pop_order(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        self.remove_order(order_id)
        self.save()
        return order


__all__ = ['OrderManager']
