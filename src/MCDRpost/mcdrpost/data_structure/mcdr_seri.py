import re
from typing import Any

from mcdreforged import Serializable


class Item(Serializable):
    """物品数据类，表示 Minecraft 中的物品

    .. note::
        Minecraft 1.20.5 之后的 components 数据和之前的 tag 标签都存放在 components中

    .. versionadded:: 3.4.1
        新增验证功能
    """

    id: str
    """物品的唯一标识符"""

    count: int
    """物品数量"""

    components: dict
    """物品的组件信息或标签"""

    def validate_attribute(self, attr_name: str, attr_value: Any, **kwargs):
        if attr_name == "id":
            attr_value: str

            if ":" not in attr_value:
                raise ValueError(f"Invalid item: no namespace ({attr_value})")
            namespace, name = attr_value.split(":")
            # https://zh.minecraft.wiki/w/%E5%91%BD%E5%90%8D%E7%A9%BA%E9%97%B4ID
            if not re.match(r"[a-z0-9_\-.]+", namespace):
                raise ValueError(f"Invalid item: invalid namespace with illegal char(s) ({namespace})")
            if not re.match(r"[a-z0-9_\-./]+", name):
                raise ValueError(f"Invalid item: invalid item name with illegal char(s) ({name})")
            return

        if attr_name == "count" and attr_value <= 0:
            raise ValueError(f"Invalid item: count must be positive ({attr_value})")


class OrderInfo(Serializable):
    """订单信息"""

    time: str
    """创建时间"""

    sender: str
    """寄件人"""

    receiver: str
    """收件人"""

    comment: str
    """备注"""

    item: Item
    """物品"""


class Order(Serializable):
    """订单"""

    id: int
    """订单唯一标识符"""

    time: str
    """创建时间"""

    sender: str
    """寄件人"""

    receiver: str
    """收件人"""

    comment: str
    """备注"""

    item: Item
    """物品"""

    def validate_attribute(self, attr_name: str, attr_value: Any, **kwargs):
        if attr_name == "id" and attr_value <= 0:
            raise ValueError(f"Invalid order: id must be positive (found {attr_value})")


class OrderData(Serializable):
    """订单数据存储结构

    orders.json 的结构在这里定义
    """

    players: list[str] = []
    """已注册玩家名单"""

    orders: dict[str, Order] = {}
    """订单数据"""
