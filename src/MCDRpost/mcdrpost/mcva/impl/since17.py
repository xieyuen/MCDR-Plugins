from mcdrpost.constants import Commands
from mcdrpost.core.services.mcva_service import MCVersionAdaptorService
from mcdrpost.data_structure import Item
from mcdrpost.mcva.abstract_adaptor import BuiltinAdaptor
from mcdrpost.mcva.environment import Environment


class Since17Adaptor(BuiltinAdaptor):
    @staticmethod
    def dict2item(item: dict) -> Item:
        return Item(id=item["id"], count=item["Count"], components=item.get("tag", {}))

    def get_replace_command(self, player: str, item: Item) -> str:
        return Commands.REPLACE_NEW.format(player, self.item2str(item))

    @staticmethod
    def is_usable(env: Environment) -> bool:
        return "1.17" <= env.mc_version < "1.20.5"

    @staticmethod
    def item2str(item: Item) -> str:
        return f"{item.id}{item.components} {item.count}"


MCVersionAdaptorService.register_adaptor(Since17Adaptor())
