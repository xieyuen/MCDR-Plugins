from mcdrpost.constants import Commands, Sounds
from mcdrpost.version_handler.sound_player.abstract_sound_player import (
    AbstractSoundPlayer,
)


class OldSoundPlayer(AbstractSoundPlayer):
    """1.13 以下版本的音效播放器"""

    def successfully_receive(self, player: str):
        self.server.execute(
            Commands.PLAY_SOUND_OLD.format(player, Sounds.SUCCESSFULLY_RECEIVE)
        )

    def successfully_post(self, sender: str, receiver: str):
        self.server.execute(
            Commands.PLAY_SOUND_OLD.format(sender, Sounds.SUCCESSFULLY_POST_SENDER)
        )
        self.server.execute(
            Commands.PLAY_SOUND_OLD.format(receiver, Sounds.SUCCESSFULLY_POST_RECEIVER)
        )

    def has_something_to_receive(self, player: str):
        self.server.execute(
            Commands.PLAY_SOUND_OLD.format(player, Sounds.HAS_SOMETHING_TO_RECEIVE)
        )


class NewSoundPlayer(AbstractSoundPlayer):
    """1.13 及以上版本的音效播放器"""

    def successfully_receive(self, player: str):
        self.server.execute(
            Commands.PLAY_SOUND_NEW.format(player, Sounds.SUCCESSFULLY_RECEIVE)
        )

    def successfully_post(self, sender: str, receiver: str):
        self.server.execute(
            Commands.PLAY_SOUND_NEW.format(sender, Sounds.SUCCESSFULLY_POST_SENDER)
        )
        self.server.execute(
            Commands.PLAY_SOUND_NEW.format(receiver, Sounds.SUCCESSFULLY_POST_RECEIVER)
        )

    def has_something_to_receive(self, player: str):
        self.server.execute(
            Commands.PLAY_SOUND_NEW.format(player, Sounds.HAS_SOMETHING_TO_RECEIVE)
        )
