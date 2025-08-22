from typing import TypedDict

from mcdreforged.api.utils import Serializable


class OrderInfo(Serializable):
    time: str
    sender: str
    receiver: str
    item: str
    comment: str


class OrderInfoDict(TypedDict):
    time: str
    sender: str
    receiver: str
    item: str
    comment: str


class Order(OrderInfo):
    id: int


class OrderData(Serializable):
    """
    订单数据

    .. note::
        ``orders`` 使用 ``dict`` 而不是 ``list`` 是因为管理更加方便

    Attributes:
        players (list[str]): 已注册的玩家名单
        orders (dict[str, Order]): 中转站内的所有订单
    """
    players: list[str] = []
    orders: dict[str, Order] = {}
