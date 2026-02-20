from typing import Any

from mcdreforged import *

psi = ServerInterface.psi()


class Config(Serializable):
    enable: bool = True
    """是否启用插件"""

    waiting_time: float = 60
    """等待时间, 超时之后才强制关闭服务器, 单位为秒"""

    def validate_attribute(self, attr_name: str, attr_value: Any, **kwargs):
        if attr_name == "waiting_time":
            if attr_value <= 0:
                raise ValueError(f"配置项 waiting_time 必须是正值, 实际配置: {attr_value}")
            if attr_value <= 3:
                psi.logger.warning(f"配置项 waiting_time 单位为秒, 实际配置 {attr_value} 可能过小")
