"""
播放提示音
"""
from mcdreforged.api.types import PluginServerInterface


def receive(server: PluginServerInterface, player: str):
    server.execute(f'execute at {player} run playsound minecraft:entity.bat.takeoff player {player}')


def successfully_post(server: PluginServerInterface, sender: str, receiver: str):
    server.execute(f'execute at {sender} run playsound minecraft:entity.arrow.hit_player player {sender}')
    server.execute(f'execute at {receiver} run playsound minecraft:entity.arrow.shoot player {receiver}')


def has_something_to_receive(server: PluginServerInterface, player: str):
    server.execute(f'execute at {player} run playsound minecraft:entity.arrow.hit_player player {player}')
