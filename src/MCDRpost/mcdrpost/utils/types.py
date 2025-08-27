from typing import Protocol

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


class ReplaceFunction(Protocol):
    def __call__(self, server: PluginServerInterface, player: str, item: Item) -> None: ...


class Item2StrFunction(Protocol):
    def __call__(self, item: Item) -> str: ...


class Dict2ItemFunction(Protocol):
    def __call__(self, item: dict) -> Item: ...
