from mcdreforged import RTextBase, RTextMCDRTranslation, ServerInterface


class TranslationKeyItem:
    """MCDRpost 翻译键

    用于封装翻译键的类，提供便捷的翻译文本获取方法。

    Attributes:
        key (str): 完整的翻译键，格式为 "mcdrpost.{value}"
        value (str): 翻译键的值部分
    """

    __FULL_KEY_TEMPLATE: str = "mcdrpost.{key}"
    __tr = ServerInterface.si().tr
    __rtr = ServerInterface.si().rtr

    def __init__(self, value: str):
        self.key = self.__FULL_KEY_TEMPLATE.format(key=value)
        self.value = value

    def tr(self, *args) -> str | RTextBase:
        """获取普通翻译，等同于 ``ServerInterface.si().tr(key_item.key, *args)``

        Args:
            *args: 传递给翻译字符串的参数

        Returns:
            str | RTextBase: 翻译后的文本或 RText 对象
        """
        return self.__tr(self.key, *args)

    def rtr(self, *args) -> RTextMCDRTranslation:
        """获取 RText 翻译，等同于 ``ServerInterface.si().rtr(key_item.key, *args)``

        Args:
            *args: 传递给翻译字符串的参数

        Returns:
            RTextMCDRTranslation: 包含翻译键的RText对象
        """
        return self.__rtr(self.key, *args)


class TranslationKeys:
    """MCDRpost 翻译键"""

    # basic
    description = TranslationKeyItem("mcdrpost.basic.description")
    info = TranslationKeyItem("mcdrpost.basic.info")

    # config
    config_loaded = TranslationKeyItem("mcdrpost.config.loaded")
    config_reloaded = TranslationKeyItem("mcdrpost.config.reloaded")

    # data
    data_loaded = TranslationKeyItem("mcdrpost.data.loaded")
    data_saved = TranslationKeyItem("mcdrpost.data.saved")
    data_validation_failed = TranslationKeyItem("mcdrpost.data.validation_failed")
    data_auto_fix = TranslationKeyItem("mcdrpost.data.auto_fix")

    # deprecation
    deprecation_info = TranslationKeyItem("mcdrpost.deprecation.info")
    deprecation_replacement_info = TranslationKeyItem("mcdrpost.deprecation.replacement_info")
    deprecation_final = TranslationKeyItem("mcdrpost.deprecation.final")

    # event
    hover = TranslationKeyItem("mcdrpost.event.hover")
    on_new_player_joined = TranslationKeyItem("mcdrpost.event.on_new_player_joined")
    on_old_player_joined = TranslationKeyItem("mcdrpost.event.on_old_player_joined")

    # rcon
    rcon_not_running = TranslationKeyItem("mcdrpost.rcon_not_running")

    # command - post
    post_default_comment = TranslationKeyItem("mcdrpost.command.post.default_comment")
    post_success_sender = TranslationKeyItem("mcdrpost.command.post.success.sender")
    post_success_receiver = TranslationKeyItem("mcdrpost.command.post.success.receiver")
    post_fail_reached_max_storage = TranslationKeyItem("mcdrpost.command.post.fail.reached_max_storage")
    post_fail_send_to_self = TranslationKeyItem("mcdrpost.command.post.fail.send_to_self")
    post_fail_invalid_item = TranslationKeyItem("mcdrpost.command.post.fail.invalid_item")
    post_fail_receiver_unregistered = TranslationKeyItem("mcdrpost.command.post.fail.receiver_unregistered")

    # command - receive
    receive_success = TranslationKeyItem("mcdrpost.command.receive.success")
    receive_fail_no_order = TranslationKeyItem("mcdrpost.command.receive.fail.no_order")
    receive_fail_no_right = TranslationKeyItem("mcdrpost.command.receive.fail.no_right")
    receive_fail_hands_not_cleared = TranslationKeyItem("mcdrpost.command.receive.fail.hands_not_cleared")
    receive_fail_undefined_id = TranslationKeyItem("mcdrpost.command.receive.fail.undefined_id")

    # command - cancel
    cancel_success = TranslationKeyItem("mcdrpost.command.cancel.success")
    cancel_fail_no_order = TranslationKeyItem("mcdrpost.command.cancel.fail.no_order")
    cancel_fail_no_right = TranslationKeyItem("mcdrpost.command.cancel.fail.no_right")
    cancel_fail_hands_not_cleared = TranslationKeyItem("mcdrpost.command.cancel.fail.hands_not_cleared")
    cancel_fail_undefined_id = TranslationKeyItem("mcdrpost.command.cancel.fail.undefined_id")

    # command - list all
    list_all_none = TranslationKeyItem("mcdrpost.command.list.all.none")
    list_all_title = TranslationKeyItem("mcdrpost.command.list.all.title")

    # command - list post
    list_post_none = TranslationKeyItem("mcdrpost.command.list.post.none")
    list_post_title = TranslationKeyItem("mcdrpost.command.list.post.title")
    list_post_cancel_tip = TranslationKeyItem("mcdrpost.command.list.post.cancel_tip")

    # command - list receive
    list_receive_none = TranslationKeyItem("mcdrpost.command.list.receive.none")
    list_receive_title = TranslationKeyItem("mcdrpost.command.list.receive.title")
    list_receive_tip = TranslationKeyItem("mcdrpost.command.list.receive.receive_tip")

    # command - list players
    list_players_none = TranslationKeyItem("mcdrpost.command.list.player.none")
    list_players_title = TranslationKeyItem("mcdrpost.command.list.player.title")

    # command - player
    player_registered = TranslationKeyItem("mcdrpost.command.player.registered")
    player_removed = TranslationKeyItem("mcdrpost.command.player.removed")
    player_fail_already_registered = TranslationKeyItem("mcdrpost.command.player.fail.already_registered")
    player_fail_unable_del = TranslationKeyItem("mcdrpost.command.player.fail.unable_del")

    # command - error
    error_incomplete_general = TranslationKeyItem("mcdrpost.command.error.incomplete.general")
    error_incomplete_receiver = TranslationKeyItem("mcdrpost.command.error.incomplete.receiver")
    error_incomplete_order_id = TranslationKeyItem("mcdrpost.command.error.incomplete.order_id")
    error_player_only = TranslationKeyItem("mcdrpost.command.error.player_only")
    error_no_perm = TranslationKeyItem("mcdrpost.command.error.no_perm")

    # command - help
    help_title = TranslationKeyItem("mcdrpost.command.help.title")

    help_info_help = TranslationKeyItem("mcdrpost.command.help.info.help")
    help_info_post = TranslationKeyItem("mcdrpost.command.help.info.post")
    help_info_receive_list = TranslationKeyItem("mcdrpost.command.help.info.receive_list")
    help_info_receive = TranslationKeyItem("mcdrpost.command.help.info.receive")
    help_info_post_list = TranslationKeyItem("mcdrpost.command.help.info.post_list")
    help_info_cancel = TranslationKeyItem("mcdrpost.command.help.info.cancel")
    help_info_list_players = TranslationKeyItem("mcdrpost.command.help.info.list_players")
    help_info_list_orders = TranslationKeyItem("mcdrpost.command.help.info.list_orders")
    help_info_player_add = TranslationKeyItem("mcdrpost.command.help.info.player.add")
    help_info_player_remove = TranslationKeyItem("mcdrpost.command.help.info.player.remove")
    help_usage_post = TranslationKeyItem("mcdrpost.command.help.usage.post")
    help_usage_receive = TranslationKeyItem("mcdrpost.command.help.usage.receive")
    help_usage_cancel = TranslationKeyItem("mcdrpost.command.help.usage.cancel")
    help_usage_player_add = TranslationKeyItem("mcdrpost.command.help.usage.player.add")
    help_usage_player_remove = TranslationKeyItem("mcdrpost.command.help.usage.player.remove")