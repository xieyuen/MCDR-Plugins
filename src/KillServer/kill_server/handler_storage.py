from dowhen.handler import EventHandler
from mcdreforged import PluginEvent

from kill_server.events.server_event import ServerEvents


class HandlerStorage:
    handlers: dict[str, EventHandler] = {}

    def register(self, e: PluginEvent, handler: EventHandler):
        if e.id in self.handlers:
            raise KeyError(e.id)
        if handler.removed:
            raise ValueError(f"An removed handler cannot be registered ({e})")
        self.handlers[e.id] = handler

    def remove(self, *events: PluginEvent):
        """删除事件监听器, 无参则全删"""
        if not events:
            events = ServerEvents.get_event_list()

        for e in events:
            if e.id not in self.handlers:
                continue

            handler = self.handlers[e.id]
            if not handler.removed:
                handler.remove()
            del self.handlers[e.id]
