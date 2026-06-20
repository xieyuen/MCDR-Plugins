"""
MCDRpost - 一个用于邮寄/传送物品的 MCDR 插件

.. versionadded:: 4.0.0
    重构为服务化架构
"""

from mcdrpost.core.main import MCDRpostMain
from mcdrpost.data_structure import Item, Order, OrderData, OrderInfo

__all__ = [
    "MCDRpostMain",
    "Item",
    "Order",
    "OrderInfo",
    "OrderData",
]
