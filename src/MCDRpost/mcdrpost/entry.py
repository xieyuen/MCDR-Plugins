from mcdreforged import PluginServerInterface

from mcdrpost.core.main import MCDRpostMain

main: MCDRpostMain


def on_load(server: PluginServerInterface, old_):
    global main
    main = MCDRpostMain(server)
    main.run()
