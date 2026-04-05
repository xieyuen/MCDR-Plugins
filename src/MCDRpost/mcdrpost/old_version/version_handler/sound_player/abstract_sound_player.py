from abc import ABC, abstractmethod
from typing import final

from mcdreforged import PluginServerInterface


class AbstractSoundPlayer(ABC):
    """音效播放

    Attributes:
        server (PluginServerInterface): MCDR 服务器接口
    """

    @final
    def __init__(self, server: PluginServerInterface):
        self.server = server

    @abstractmethod
    def successfully_receive(self, player: str):
        """播放音效: 当成功接受订单时

        Args:
            player (str): 玩家 id
        """
        raise NotImplementedError

    @abstractmethod
    def successfully_post(self, sender: str, receiver: str):
        """播放音效: 当成功发送订单时

        请给收件人和发件人播放音效

        Args:
            sender (str): 发件人
            receiver (str): 收件人

        Returns:

        """
        raise NotImplementedError

    @abstractmethod
    def has_something_to_receive(self, player: str):
        """播放音效: 登陆后发现有订单未接受时

        Args:
            player (str): 玩家 id
        """
        raise NotImplementedError
