from typing import Literal

from mcdrpost.data_structure import Item

PLUGIN_ID: Literal["mcdrpost"] = "mcdrpost"
CONFIG_FILE_NAME: Literal['config.yml'] = 'config.yml'
CONFIG_FILE_TYPE: Literal["yaml"] = "yaml"
ORDERS_DATA_FILE_NAME: Literal["orders.json"] = 'orders.json'
ORDERS_DATA_FILE_TYPE: Literal["json"] = "json"

OFFHAND_CODE = 'Inventory[{Slot:-106b}]'

AIR = Item(id='minecraft:air', count=1)

END_LINE = '\n'
