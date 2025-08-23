from mcdreforged import PluginServerInterface

__all__ = ['Tags', 'tr']


def tr(tag: str, *args):
    """translation"""
    return PluginServerInterface.get_instance().tr(f'mcdrpost.{tag}', *args)


class Tags:
    desc = 'desc'
    info_msg = 'info_msg'
    hover = 'hover'
    new_player_joined = 'new_player_joined'

    class help:
        title = 'help.title'
        hint_help = 'help.hint_help'
        hint_p = 'help.hint_p'
        hint_rl = 'help.hint_rl'
        hint_r = 'help.hint_r'
        hint_pl = 'help.hint_pl'
        hint_c = 'help.hint_c'
        hint_ls_players = 'help.hint_ls_players'
        hint_ls_orders = 'help.hint_ls_orders'
        hint_player_add = 'help.hint_player_add'
        hint_player_remove = 'help.hint_player_remove'
        p = 'help.p'
        r = 'help.r'
        c = 'help.c'
        player_add = 'help.player_add'
        player_remove = 'help.player_remove'

    no_datafile = 'no_datafile'
    clear_offhand = 'clear_offhand'
    no_comment = 'no_comment'
    at_max_storage = 'at_max_storage'
    no_receiver = 'no_receiver'
    same_person = 'same_person'
    check_offhand = 'check_offhand'
    reply_success_post = 'reply_success_post'
    hint_receive = 'hint_receive'

    no_post_orders = 'no_post_orders'
    list_post_orders_title = 'list_post_orders_title'
    hint_cancel = 'hint_cancel'

    not_receiver = 'not_receiver'
    unchecked_orderid = 'unchecked_orderid'
    receive_success = 'receive_success'

    no_receive_orders = 'no_receive_orders'
    list_receive_orders_title = 'list_receive_orders_title'
    hint_order_receive = 'hint_order_receive'

    no_sender = 'no_sender'
    cancel_success = 'cancel_success'
    list_player_title = 'list_player_title'
    no_orders = 'no_orders'
    list_orders_title = 'list_orders_title'

    has_player = 'has_player'
    login_success = 'login_success'
    login_log = 'login_log'
    cannot_del_player = 'cannot_del_player'
    del_player_success = 'del_player_success'
    del_player_log = 'del_player_log'

    only_for_player = 'only_for_player'
    no_permission = 'no_permission'
    no_input_receiver = 'no_input_receiver'
    no_input_receive_orderid = 'no_input_receive_orderid'
    no_input_cancel_orderid = 'no_input_cancel_orderid'
    command_incomplete = 'command_incomplete'

    wait_for_receive = 'wait_for_receive'

    class config:
        class display:
            max_storage = 'config.display.max_storage'
            allow_alias = 'config.display.allow_alias'
            command_prefix = 'config.display.command_prefix'
            auto_fix = 'config.display.auto_fix'
            receive_tip_delay = 'config.display.receive_tip_delay'

        load = 'config.load'
        save = 'config.save'

    class data:
        load = 'data.load'
        save = 'data.save'

    class error:
        invalid_order = 'error.invalid_order'

    class auto_fix:
        invalid_order = 'auto_fix.invalid_order'

    class rcon:
        not_running = 'rcon.not_running'

    class env:
        server_no_start = 'env.server_no_start'
        version = 'env.version'