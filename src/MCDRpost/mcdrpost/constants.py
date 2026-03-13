from typing import Literal

from mcdrpost.data_structure import Item

PLUGIN_ID: Literal["mcdrpost"] = "mcdrpost"
CONFIG_FILE_NAME: Literal["config.yml"] = "config.yml"
CONFIG_FILE_TYPE: Literal["yaml"] = "yaml"
ORDER_DATA_FILE_NAME: Literal["orders.json"] = "orders.json"
ORDERS_DATA_FILE_TYPE: Literal["json"] = "json"

SIMPLE_HELP_MESSAGE = {
    "en_us": "post/teleport weapon hands items",
    "zh_cn": "传送/收寄副手物品",
}

OFFHAND_CODE: Literal["Inventory[{Slot:-106b}]"] = "Inventory[{Slot:-106b}]"

AIR: Item = Item(id="minecraft:air", count=1, components={})

END_LINE: Literal["\n"] = "\n"


class Deprecations:
    TEMPLATE = "{} is deprecated in v{}, and will be removed in v{}."
    INSTEAD_INFO_TEMPLATE = "Please use {} instead."


class Commands:
    REPLACE_OLD = "replaceitem entity {0} weapon.offhand {1}"
    REPLACE_NEW = "item replace entity {0} weapon.offhand with {1}"
    GET_ITEM = "data get entity {0} Inventory[{Slot:-106b}]"
    PLAY_SOUND_NEW = "execute at {0} run {1} player {0}"
    PLAY_SOUND_OLD = "execute {0} ~ ~ ~ playsound {1} player {0}"


class Sounds:
    SUCCESSFULLY_RECEIVE = "minecraft:entity.bat.takeoff"
    SUCCESSFULLY_POST_SENDER = "minecraft:entity.arrow.hit_player"
    SUCCESSFULLY_POST_RECEIVER = "minecraft:entity.arrow.shoot"
    HAS_SOMETHING_TO_RECEIVE = "minecraft:entity.arrow.hit_player"
