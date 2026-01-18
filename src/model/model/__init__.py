from mcdreforged import PluginServerInterface

from model.plotter import Plotter
from src.model.model.command import CommandRegister


def on_load(server: PluginServerInterface, _old):
    CommandRegister(server, Plotter(server)).register()
