from typing import Literal

from mcdrpost.data_structure import Item

PLUGIN_ID: Literal["mcdrpost"] = "mcdrpost"
CONFIG_FILE_NAME: Literal['config.yml'] = 'config.yml'
CONFIG_FILE_TYPE: Literal["yaml"] = "yaml"
ORDER_DATA_FILE_NAME: Literal["orders.json"] = 'orders.json'
ORDERS_DATA_FILE_TYPE: Literal["json"] = "json"

SIMPLE_HELP_MESSAGE = {
    "en_us": "post/teleport weapon hands items",
    "zh_cn": "传送/收寄副手物品",
}

OFFHAND_CODE = 'Inventory[{Slot:-106b}]'

AIR = Item(id='minecraft:air', count=1, components={})

END_LINE = '\n'
