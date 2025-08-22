from typing import Protocol

from mcdreforged.api.types import PluginServerInterface


class ReplaceFunction(Protocol):
    def __call__(self, server: PluginServerInterface, player: str, item: str) -> None: ...
