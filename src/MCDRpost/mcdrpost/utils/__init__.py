import json
import time

from mcdreforged.api.types import PluginServerInterface

from mcdrpost import constants
from mcdrpost.utils.translation_tags import Tags


def get_formatted_time() -> str:
    """获取当前时间的格式化的字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_offhand_item(server: PluginServerInterface, player: str) -> dict | None:
    """获取玩家副手物品，建议开启 Rcon

    Args:
        server (PluginServerInterface): MCDR插件接口
        player (str): 玩家名

    Returns:
        dict | None: 物品信息，若获取失败或返回 None
    """
    # api = server.get_plugin_instance('minecraft_data_api')
    import minecraft_data_api as api

    try:
        if server.is_rcon_running():
            offhand_item = api.convert_minecraft_json(
                server.rcon_query(f'data get entity {player} {constants.OFFHAND_CODE}')
            )
        else:
            server.logger.warning(tr(Tags.rcon.not_running))
            offhand_item = api.get_player_info(player, constants.OFFHAND_CODE)

        if isinstance(offhand_item, dict):
            return offhand_item

    except Exception as e:
        server.logger.error(f"Error occurred during getting {player}'s offhand item")
        server.logger.error(e)


def get_formatted_item(item_json: dict) -> str:
    item_tag = item_json.get("tag", "")
    return f"{item_json['id']}" + json.dumps(item_tag, ensure_ascii=False) + f"{item_json.get('Count', '')}"


def tr(tag: str, *args):
    """translation"""
    return PluginServerInterface.get_instance().tr(f'mcdrpost.{tag}', *args)


__all__ = ['get_formatted_time', 'get_offhand_item', 'get_formatted_item', 'tr']
