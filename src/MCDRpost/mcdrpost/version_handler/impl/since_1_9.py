from typing import override

from mcdreforged import new_thread

import minecraft_data_api as api
from mcdrpost import constants
from mcdrpost.data_structure import Item
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.version_handler.abstract_version_handler import BuiltinVersionHandler


class Since9Handler(BuiltinVersionHandler):
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

    @override
    def get_offhand_item(self, player: str) -> Item:
        @new_thread('MCDRpost | get offhand item')
        def get():
            return api.get_player_info(player, constants.OFFHAND_CODE)

        # 等待异步执行完成并获取返回值
        offhand_item = get().get_return_value(block=True)

        return Item(
            id=offhand_item['id'],
            count=offhand_item['Count'],
            components=offhand_item.get('tag', {})
        )


VersionManager.register_handler(Since9Handler, lambda env: '1.9' <= env.server_version < "1.13")
