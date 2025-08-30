from typing import override

from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler


class Since17Handler(AbstractVersionHandler):
    def __init__(self, server: PluginServerInterface):
        self.server = server

    @staticmethod
    @override
    def dict2item(item: dict) -> Item:
        return Item(
            id=item['id'],
            count=item['Count'],
            components=item.get('tag', {})
        )

    @staticmethod
    @override
    def item2str(item: Item) -> str:
        return f'{item.id}{item.components} {item.count}'

    @override
    def replace(self, player: str, item: str) -> None:
        self.server.execute(f'item replace entity {player} weapon.offhand with {item}')
