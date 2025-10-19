from typing import override

from mcdrpost.data_structure import Item
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.version_handler.abstract_version_handler import BuiltinVersionHandler


class Since13Handler(BuiltinVersionHandler):
    @override
    def replace(self, player: str, item: str) -> None:
        self.server.execute(f"replaceitem entity {player} weapon.offhand {item}")

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


VersionManager.register_handler(
    Since13Handler,
    lambda env: (1, 13) <= env.server_version < (1, 17)
)
