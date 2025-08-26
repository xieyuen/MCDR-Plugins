"""数据结构模块，定义了插件中使用的核心数据类"""

from mcdreforged import Serializable


class Item(Serializable):
    """物品数据类，表示 Minecraft 中的物品

    Attributes:
        components (dict[str, dict]): 物品的组件数据（1.20.5+版本特性，对于低版本这里储存对应的 tag）
        count (int): 物品数量
        id (str): 物品ID
    """
    components: dict[str, dict]
    count: int
    id: str


class OrderInfo(Serializable):
    """订单信息

    Attributes:
        comment (str): 订单备注信息
        item (Item): 订单中的物品
        receiver (str): 收件人
        sender (str): 发件人
        time (str): 订单创建时间
    """
    comment: str
    item: Item
    receiver: str
    sender: str
    time: str


class Order(OrderInfo):
    """订单

    Attributes:
        id (int): 订单唯一标识符
        comment (str): 订单备注信息
        item (Item): 订单中的物品
        receiver (str): 收件人
        sender (str): 发件人
        time (str): 订单创建时间
    """
    id: int


class OrderData(Serializable):
    """订单数据类，包含所有订单和注册玩家信息

    Attributes:
        orders (dict[str, Order]): 所有订单的字典，以订单ID为键，订单对象为值
        players (list[str]): 已注册玩家列表
    """
    orders: dict[str, Order] = {}
    players: list[str] = []