from typing import override

from mcdrpost.data_structure import Item
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler


class Since20Handler(AbstractVersionHandler):
    @override
    def replace(self, player: str, item: str) -> None:
        self.server.execute(f'item replace entity {player} weapon.offhand with {item}')

    @staticmethod
    @override
    def dict2item(item: dict) -> Item:
        return Item(
            id=item['id'],
            count=item['count'],
            components=item.get('components', {})
        )

    @staticmethod
    @override
    def item2str(item: Item) -> str:
        if not item.components:
            return f"{item.id} {item.count}"
        components_str = '['
        for k, v in item.components.items():
            components_str += f' {k}={v},'
        components_str += ']'
        return f'{item.id}{components_str} {item.count}'


VersionManager.register_handler(Since20Handler, lambda env: env.server_version >= "1.20.5")
