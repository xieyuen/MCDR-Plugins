import minecraft_data_api as api
from mcdrpost.constants import OFFHAND_CODE
from mcdrpost.data_structure import Item
from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler


class DefaultVersionHandler(AbstractVersionHandler):
    """默认处理器"""

    def get_offhand_item(self, player: str) -> Item:
        item = api.convert_minecraft_json(
            self.server.rcon_query(f'data get entity {player} {OFFHAND_CODE}')
        )

        return Item(
            id=item['id'],
            count=item['Count'],
            components=item.get('tag', {})
        )

    def replace(self, player: str, item: Item) -> None:
        self.server.execute(f'item replace entity {player} {OFFHAND_CODE} with {self.item2str(item)}')

    @staticmethod
    def item2str(item: Item) -> str:
        return f'{item.id}{item.components} {item.count}'
