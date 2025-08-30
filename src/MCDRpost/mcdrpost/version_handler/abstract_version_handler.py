from abc import ABC, abstractmethod

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


class AbstractVersionHandler(ABC):
    server: PluginServerInterface

    @abstractmethod
    def replace(self, player: str, item: str) -> None: ...

    @staticmethod
    @abstractmethod
    def dict2item(item: dict) -> Item: ...

    @staticmethod
    @abstractmethod
    def item2str(item: Item) -> str: ...
