from typing import TYPE_CHECKING

from mcdrpost.data_structure import OrderInfo
from mcdrpost.utils import get_formatted_time

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class PostManager:
    def __init__(self, mcdrpost: "MCDRpostMain"):
        self.mcdrpost = mcdrpost
        self.server = self.mcdrpost.server

    def sent(self, sender: str, receiver: str, comment: str | None = None) -> int:
        """发送订单

        Args:
            sender (str):  发件人
            receiver (str): 收件人
            comment (str, optional): 备注

        Returns:
            int: 订单号
        """

        item = ...

        info = OrderInfo(
            time=get_formatted_time(),
            sender=sender,
            receiver=receiver,
        )
        raise NotImplementedError
