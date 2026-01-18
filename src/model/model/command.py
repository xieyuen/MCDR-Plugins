from mcdreforged import PluginServerInterface

from src.model.model import Plotter


class CommandRegister:
    def __init__(self, server: PluginServerInterface, plotter: Plotter):
        self.server = server
        self.logger = server.logger
        self.plotter = plotter

    def register(self):
        raise NotImplementedError
