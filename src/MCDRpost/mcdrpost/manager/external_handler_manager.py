from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost.version_handler.abstract_version_handler import AbstractVersionHandler

if TYPE_CHECKING:
    from mcdrpost.coordinator import MCDRpostCoordinator


class ExternalHandlerManager:
    """
    This class manages the external handlers.
    """
    __external_handlers: list[type[AbstractVersionHandler]] = []

    def __init__(self, coo: "MCDRpostCoordinator"):
        self.coo: "MCDRpostCoordinator" = coo
        self._server: PluginServerInterface = coo.server
        self.logger = self._server.logger

    def register(self, handler: type[AbstractVersionHandler]):
        self.__external_handlers.append(handler)
