"""数据结构模块，定义了插件中使用的核心数据类

.. versionadded:: 3.4.1
    新增 pydantic 支持和数据验证功能

    验证功能不影响 ``auto_fix`` 配置, 只验证无法修复的内容, 如无效的命名空间 ID
"""

try:
    from .pydantic_model import Item, OrderInfo, Order, OrderData
except ImportError:
    from .mcdr_seri import Item, OrderInfo, Order, OrderData

__all__ = ["Item", "OrderInfo", "Order", "OrderData"]
