import re

from pydantic import BaseModel, Field, PositiveInt, field_validator
from typing_extensions import Self


class Item(BaseModel):
    """物品数据类，表示 Minecraft 中的物品

    .. note::
        Minecraft 1.20.5 之后的 components 数据和之前的 tag 标签都存放在 components中

    .. versionadded:: 3.4.1
        新增验证功能
    """

    id: str
    """物品的唯一标识符"""

    count: PositiveInt
    """物品数量"""

    components: dict = Field(default_factory=dict)
    """物品的组件信息或标签"""

    @field_validator('id')
    @classmethod
    def validate_id(cls, value: str) -> Self:
        if ":" not in value:
            raise ValueError(f"Invalid item: no namespace ({value})")
        namespace, name = value.split(":")
        # https://zh.minecraft.wiki/w/%E5%91%BD%E5%90%8D%E7%A9%BA%E9%97%B4ID
        if not re.match(r"[a-z0-9_\-.]+", namespace):
            raise ValueError(f"Invalid item: invalid namespace with illegal char(s) ({namespace})")
        if not re.match(r"[a-z0-9_\-./]+", name):
            raise ValueError(f"Invalid item: invalid item name with illegal char(s) ({name})")
        return value


class OrderInfo(BaseModel):
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


class Order(BaseModel):
    """订单"""

    id: PositiveInt
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


class OrderData(BaseModel):
    """订单数据存储结构

    orders.json 的结构在这里定义
    """

    players: list[str] = Field(default_factory=list)
    """已注册玩家名单"""

    orders: dict[str, Order] = Field(default_factory=dict)
    """订单数据"""
