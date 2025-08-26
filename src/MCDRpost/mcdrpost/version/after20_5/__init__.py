from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


def replace(server: PluginServerInterface, player: str, item: str):
    server.execute(f'item replace entity {player} weapon.offhand with {item}')


def dict2item(item: dict) -> Item:
    return Item(
        id=item['id'],
        count=item['count'],
        components=item.get('components', {})
    )


def item2str(item: Item) -> str:
    comp_str = '['
    for k, v in item.components.items():
        comp_str += f' {k}={v},'
    comp_str += ']'
    return f'{item.id}{comp_str} {item.count}'
