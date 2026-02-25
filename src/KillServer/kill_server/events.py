from mcdreforged import LiteralEvent

ServerStoppingEvent = LiteralEvent("kill_server.server_stopping")
PluginStoppingServerEvent = LiteralEvent("kill_server.plugin_stopping_server")
WorldSavedEvent = LiteralEvent("kill_server.world_saved")

__all__ = ["ServerStoppingEvent", "PluginStoppingServerEvent", "WorldSavedEvent"]
