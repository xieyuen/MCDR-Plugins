from mcdrpost.version_handler.sound_player.abstract_sound_player import AbstractSoundPlayer


class OldSoundPlayer(AbstractSoundPlayer):
    """1.13 以下版本的音效播放器"""
    def successfully_receive(self, player: str):
        self.server.execute(f'execute {player} ~ ~ ~ playsound minecraft:entity.bat.takeoff player {player}')

    def successfully_post(self, sender: str, receiver: str):
        self.server.execute(f'execute {sender} ~ ~ ~ playsound minecraft:entity.arrow.hit_player player {sender}')
        self.server.execute(f'execute {receiver} ~ ~ ~ playsound minecraft:entity.arrow.shoot player {receiver}')

    def has_something_to_receive(self, player: str):
        self.server.execute(f'execute {player} ~ ~ ~ playsound minecraft:entity.arrow.hit_player player {player}')


class NewSoundPlayer(AbstractSoundPlayer):
    """1.13 及以上版本的音效播放器"""
    def successfully_receive(self, player: str):
        self.server.execute(f'execute at {player} run playsound minecraft:entity.bat.takeoff player {player}')

    def successfully_post(self, sender: str, receiver: str):
        self.server.execute(f'execute at {sender} run playsound minecraft:entity.arrow.hit_player player {sender}')
        self.server.execute(f'execute at {receiver} run playsound minecraft:entity.arrow.shoot player {receiver}')

    def has_something_to_receive(self, player: str):
        self.server.execute(f'execute at {player} run playsound minecraft:entity.arrow.hit_player player {player}')
