from mcdreforged import PluginServerInterface, RTextBase, RTextMCDRTranslation


class TranslationKeyItem:
    """MCDRpost 翻译键"""

    __FULL_KEY_TEMPLATE: str = 'mcdrpost.{key}'
    __tr = PluginServerInterface.si().tr
    __rtr = PluginServerInterface.si().rtr

    def __init__(self, value: str):
        self.key = self.__FULL_KEY_TEMPLATE.format(key=value)
        self.value = value

    def tr(self, *args) -> str | RTextBase:
        """获取普通翻译，等同于 ``ServerInterface.si().tr(key_item.key, *args)``"""
        return self.__tr(self.key, *args)

    def rtr(self, *args) -> RTextMCDRTranslation:
        """获取 RText 翻译，等同于 ``ServerInterface.si().rtr(key_item.key, *args)``"""
        return self.__rtr(self.key, *args)


class TranslationKeys:
    desc = TranslationKeyItem('desc')
    info_msg = TranslationKeyItem('info_msg')
    hover = TranslationKeyItem('hover')
    new_player_joined = TranslationKeyItem('new_player_joined')

    class help:
        title = TranslationKeyItem('help.title')
        hint_help = TranslationKeyItem('help.hint_help')
        hint_p = TranslationKeyItem('help.hint_p')
        hint_rl = TranslationKeyItem('help.hint_rl')
        hint_r = TranslationKeyItem('help.hint_r')
        hint_pl = TranslationKeyItem('help.hint_pl')
        hint_c = TranslationKeyItem('help.hint_c')
        hint_ls_players = TranslationKeyItem('help.hint_ls_players')
        hint_ls_orders = TranslationKeyItem('help.hint_ls_orders')
        hint_player_add = TranslationKeyItem('help.hint_player_add')
        hint_player_remove = TranslationKeyItem('help.hint_player_remove')
        p = TranslationKeyItem('help.p')
        r = TranslationKeyItem('help.r')
        c = TranslationKeyItem('help.c')
        player_add = TranslationKeyItem('help.player_add')
        player_remove = TranslationKeyItem('help.player_remove')

    no_datafile = TranslationKeyItem('no_datafile')
    clear_offhand = TranslationKeyItem('clear_offhand')
    no_comment = TranslationKeyItem('no_comment')
    at_max_storage = TranslationKeyItem('at_max_storage')
    no_receiver = TranslationKeyItem('no_receiver')
    same_person = TranslationKeyItem('same_person')
    check_offhand = TranslationKeyItem('check_offhand')
    reply_success_post = TranslationKeyItem('reply_success_post')
    hint_receive = TranslationKeyItem('hint_receive')

    no_post_orders = TranslationKeyItem('no_post_orders')
    list_post_orders_title = TranslationKeyItem('list_post_orders_title')
    hint_cancel = TranslationKeyItem('hint_cancel')

    not_receiver = TranslationKeyItem('not_receiver')
    unchecked_orderid = TranslationKeyItem('unchecked_orderid')
    receive_success = TranslationKeyItem('receive_success')

    no_receive_orders = TranslationKeyItem('no_receive_orders')
    list_receive_orders_title = TranslationKeyItem('list_receive_orders_title')
    hint_order_receive = TranslationKeyItem('hint_order_receive')

    no_sender = TranslationKeyItem('no_sender')
    cancel_success = TranslationKeyItem('cancel_success')
    list_player_title = TranslationKeyItem('list_player_title')
    no_orders = TranslationKeyItem('no_orders')
    list_orders_title = TranslationKeyItem('list_orders_title')

    has_player = TranslationKeyItem('has_player')
    login_success = TranslationKeyItem('login_success')
    login_log = TranslationKeyItem('login_log')
    cannot_del_player = TranslationKeyItem('cannot_del_player')
    del_player_success = TranslationKeyItem('del_player_success')
    del_player_log = TranslationKeyItem('del_player_log')

    only_for_player = TranslationKeyItem('only_for_player')
    no_permission = TranslationKeyItem('no_permission')
    no_input_receiver = TranslationKeyItem('no_input_receiver')
    no_input_receive_orderid = TranslationKeyItem('no_input_receive_orderid')
    no_input_cancel_orderid = TranslationKeyItem('no_input_cancel_orderid')
    command_incomplete = TranslationKeyItem('command_incomplete')

    wait_for_receive = TranslationKeyItem('wait_for_receive')

    class config:
        load = TranslationKeyItem('config.load')
        save = TranslationKeyItem('config.save')

    class data:
        load = TranslationKeyItem('data.load')
        save = TranslationKeyItem('data.save')

    class error:
        invalid_order = TranslationKeyItem('error.invalid_order')
        running = TranslationKeyItem('error.running')

    class auto_fix:
        invalid_order = TranslationKeyItem('auto_fix.invalid_order')

    class rcon:
        not_running = TranslationKeyItem('rcon.not_running')

    class env:
        server_no_start = TranslationKeyItem('env.server_no_start')
        version = TranslationKeyItem('env.version')

    reload_success = TranslationKeyItem('reload_success')
