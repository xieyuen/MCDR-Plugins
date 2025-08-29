from mcdreforged import PluginServerInterface

from mcdrpost.data_structure import Item


def replace(server: PluginServerInterface, player: str, item: str):
    server.execute(f'item replace entity {player} weapon.offhand with {item}')


def dict2item(item: dict) -> Item:
    return Item.deserialize(item)


def item2str(item: Item) -> str:
    if not item.components:
        return f"{item.id} {item.count}"
    components_str = '['
    for k, v in item.components.items():
        components_str += f' {k}={v},'
    components_str += ']'
    return f'{item.id}{components_str} {item.count}'
