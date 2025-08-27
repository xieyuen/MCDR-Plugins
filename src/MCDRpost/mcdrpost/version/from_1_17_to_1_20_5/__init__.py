from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


def replace(server: PluginServerInterface, player: str, item: str):
    server.execute(f'item replace entity {player} weapon.offhand with {item}')


def dict2item(item: dict) -> Item:
    return Item(
        id=item['id'],
        count=item['Count'],
        components=item.get('tag', {})
    )


def item2str(item: Item) -> str:
    return f'{item.id}{item.components} {item.count}'
