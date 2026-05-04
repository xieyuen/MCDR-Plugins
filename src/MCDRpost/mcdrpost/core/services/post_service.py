from typing import TYPE_CHECKING

from mcdrpost import constants
from mcdrpost.data_structure import OrderInfo
from mcdrpost.utils import get_formatted_time

if TYPE_CHECKING:
    from mcdrpost.core.main import MCDRpostMain


class PostService:
    def __init__(self, mcdrpost: "MCDRpostMain"):
        self.mcdrpost = mcdrpost
        self.server = self.mcdrpost.server
        self.logger = self.server.logger

    def sent(self, sender: str, receiver: str, comment: str | None = None) -> int:
        """发送订单

        Args:
            sender (str):  发件人
            receiver (str): 收件人
            comment (str, optional): 备注

        Returns:
            int: 订单号
        """

        item = self.mcdrpost.mcva_service.get_offhand_item(sender)

        self.logger.debug(f"detected item from {sender}: {item}")
        self.logger.debug(f"posting...")

        self.mcdrpost.mcva_service.replace(sender, constants.AIR)

        info = OrderInfo(
            time=get_formatted_time(),
            sender=sender,
            receiver=receiver,
            item=item,
            comment=comment,
        )
        id = self.mcdrpost.data_service.create_order(info)

        # TODO: play sounds

        return id

