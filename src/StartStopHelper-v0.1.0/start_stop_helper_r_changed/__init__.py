import time

from mcdreforged import Literal, PluginServerInterface, Serializable, new_thread


class CommandPermission(Serializable):
    help = 3
    start = 3
    stop = 3
    stop_exit = 4
    restart = 3
    exit = 4
    kill = 4


class ConfigKill(Serializable):
    enable: bool = False
    timeout: float = 10


class Config(Serializable):
    permissions: CommandPermission = CommandPermission()
    kill: ConfigKill = ConfigKill()


config: Config


def stop_server(server: PluginServerInterface):
    if not config.kill.enable:
        server.stop()
        return

    @new_thread('StartStopHelperChanged|Stopper')
    def stopper():
        server.stop()
        time.sleep(config.kill.timeout)
        if server.is_server_running():
            server.logger.warning("Server is still running after timeout, force kill")
            server.kill()

    stopper()


def restart_server(server: PluginServerInterface):
    if not config.kill.enable:
        server.restart()
    else:
        stop_server(server)
        server.start()


def on_load(server: PluginServerInterface, _old_module):
    global config
    config = server.load_config_simple(target_class=Config)
    server.logger.warning("你使用的并非原版！而是 xieyuen 修改版!")
    server.logger.info("若需要原版，请在下面的网址下载（或者用MPM）")
    server.logger.info("https://www.mcdreforged.org/plugins/start_stop_helper_r")
    server.logger.info("或者用 MPM")

    server.register_help_message(
        '!!server',
        {
            'en_us': 'Start and stop server helper',
            'zh_cn': '开关服助手'
        }
    )
    server.register_command(
        Literal('!!server').
        requires(lambda src: src.has_permission(config.permissions.help)).
        runs(lambda src: src.reply(server.rtr('start_stop_helper_r.help'))
             ).
        then(
            Literal('start').
            requires(lambda src: src.has_permission(config.permissions.start)).
            runs(lambda src: server.start())
        ).
        then(
            Literal('stop').
            requires(lambda src: src.has_permission(config.permissions.stop)).
            runs(lambda src: server.stop())
        ).
        then(
            Literal('stop_exit').
            requires(
                lambda src: src.has_permission(config.permissions.stop_exit)).
            runs(lambda src: server.stop_exit())
        ).
        then(
            Literal('restart').
            requires(
                lambda src: src.has_permission(config.permissions.restart)).
            runs(lambda src: server.restart())
        ).
        then(
            Literal('exit').
            requires(lambda src: src.has_permission(config.permissions.exit)).
            runs(lambda src: server.exit())
        ).
        then(
            Literal('kill').
            requires(lambda src: src.has_permission(config.permissions.kill)).
            runs(lambda src: server.kill())
        )
    )
