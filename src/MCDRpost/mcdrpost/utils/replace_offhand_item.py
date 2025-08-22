"""替换副手物品"""

from mcdreforged.api.types import PluginServerInterface


def replace_for_17(server: PluginServerInterface, player: str, item: str) -> None:
    """使用 Minecraft 1.17+ 的 ``item`` 命令替换玩家副手物品

    Args:
        server (PluginServerInterface): MCDR插件接口
        player (str): 玩家名
        item (str): 要替换的物品 id
    """
    server.execute(f'item replace entity {player} weapon.offhand with {item}')


def replace_for_lower_17(server: PluginServerInterface, player: str, item: str) -> None:
    """使用 Minecraft 1.17 以下的 ``replaceitem`` 命令替换玩家副手物品

    Args:
        server (PluginServerInterface): MCDR插件接口
        player (str): 玩家名
        item (str): 要替换的物品 id
    """
    server.execute(f'replaceitem entity {player} weapon.offhand {item}')


__all__ = ['replace_for_17', 'replace_for_lower_17']
