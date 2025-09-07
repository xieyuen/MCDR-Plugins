from mcdreforged import PluginServerInterface, new_thread

import minecraft_data_api as api
from mcdrpost import constants
from mcdrpost.utils.translation import Tags, tr


def get_offhand_item(server: PluginServerInterface, player: str) -> dict | None:
    """获取玩家副手物品，建议开启 Rcon

    Args:
        server (PluginServerInterface): MCDR插件接口
        player (str): 玩家名

    Returns:
        dict | None: 物品信息，若获取失败或返回 None
    """
    offhand_item = None

    try:
        if server.is_rcon_running():
            offhand_item = api.convert_minecraft_json(
                server.rcon_query(f'data get entity {player} {constants.OFFHAND_CODE}')
            )
        else:
            server.logger.warning(tr(Tags.rcon.not_running))

            @new_thread('MCDRpost | get offhand item')
            def get():
                nonlocal offhand_item
                offhand_item = api.get_player_info(player, constants.OFFHAND_CODE)

            get()

        if isinstance(offhand_item, dict):
            return offhand_item

    except Exception as e:
        server.logger.error(f"Error occurred during getting {player}'s offhand item")
        server.logger.error(e)
