MCDRpost API--自定义 Handler
============================

.. py:currentmodule:: mcdrpost.api

一般来说，MCDRpost已经能够适应大多数服务端，但是对于某些特殊情况（比如1.9版本） [#f1]_，MCDRpost可能无法满足需求，
考虑到插件对 Minecraft 的兼容性，插件暴露了一定的 API 用于 Minecraft 一些特殊服务端的适配

核心 API 有:

- classes
    - :class:`AbstractVersionHandler`
    - :class:`AbstractSoundPlayer`
    - :class:`DefaultVersionHandler`
    - :class:`NewSoundPlayer`
    - :class:`OldSoundPlayer`
- functions
    - :func:`register_handler`
- types
    - :class:`Item`
    - :class:`Environment`
- constants
    - OFFHAND_CODE

你可以在导入的时候使用下面的方式：

.. code-block:: python

    from mcdrpost.api import *

当然如果不希望污染全局变量也可以这样：

.. code-block:: python

    from mcdrpost import api as mp

详细文档
*********

处理器
--------

.. autoclass:: AbstractVersionHandler
.. autoclass:: DefaultVersionHandler
.. autofunction:: register_handler

声音播放器
----------

.. autoclass:: AbstractSoundPlayer
.. autoclass:: NewSoundPlayer
.. autoclass:: OldSoundPlayer

类型
--------

.. autoclass:: Item
.. autoclass:: Environment

示例
-------

我们建议使用插件定义你的 Handler，下面是一个单文件插件的例子

.. code:: python

    PLUGIN_METADATA = {
        'id': 'example_handler',
        'version': '1.0.0',
        'name': 'Example Handler',
        'author': 'xieyuen',
        'description': 'An example of custom handler',
        'dependencies': {
            'mcdrpost': '>=3.3.2-beta5'
        }
    }


    def on_load(_server, _old):
        import minecraft_data_api as api
        from mcdrpost.api import AbstractVersionHandler, Item, OFFHAND_CODE, register_handler

        class ExampleHandler(AbstractVersionHandler):
            def replace(self, player: str, item: Item) -> None:
                self.server.execute(f'item replace entity {player} with {self.item2str(item)}')

            @staticmethod
            def item2str(item: Item) -> str:
                return f'{item.id}{item.components} {item.count}'

            @staticmethod
            def dict2item(item: dict) -> Item:
                return Item(
                    id=item['id'],
                    count=item['Count'],
                    components=item.get('tag', {})
                )

            def get_offhand_item(self, player: str) -> Item:
                item = api.convert_minecraft_json(
                    self.server.rcon_query(
                        f'data get entity {player} {OFFHAND_CODE}'
                    )
                )

                return self.dict2item(item)

        register_handler(
            ExampleHandler,
            lambda env: '1.20.5' > env.server_version >= '1.17'
        )

.. note::
   在 ``on_load()`` 函数中定义是为了保证 MCDR 能正确加载插件，
   因为 MCDR 要先读取 Metadata 才知道插件依赖 MCDRpost，而此时 MCDRpost 不一定已经被加载
   放在函数中先不运行就可以避免没有优先加载 MCDRpost 导致的问题

   **注意：如果是多文件插件就没有这种问题，放在外面定义就好**

如果是用多文件插件的话，你甚至不需要定义 ``on_load``, 只需要在入口点内定义 Handler 并注册就好

在 ``example_handler/entry.py`` 文件内

.. code:: python

    import minecraft_data_api as api
    from mcdrpost.api import AbstractVersionHandler, Item, OFFHAND_CODE, register_handler


    class ExampleHandler(AbstractVersionHandler):
        def replace(self, player: str, item: Item) -> None:
            self.server.execute(f'item replace entity {player} with {self.item2str(item)}')

        @staticmethod
        def item2str(item: Item) -> str:
            return f'{item.id}{item.components} {item.count}'

        @staticmethod
        def dict2item(item: dict) -> Item:
            return Item(
                id=item['id'],
                count=item['Count'],
                components=item.get('tag', {})
            )

        def get_offhand_item(self, player: str) -> Item:
            item = api.convert_minecraft_json(
                self.server.rcon_query(
                    f'data get entity {player} {OFFHAND_CODE}'
                )
            )

            return self.dict2item(item)


    register_handler(
        ExampleHandler,
        lambda env: '1.20.5' > env.server_version >= '1.17'
    )

.. rubric:: 脚注

.. [#f1] 1.13 以前没有 ``/data`` 命令，要获取玩家物品需要在服务端安装插件，但 MCDR 主打的就是不修改服务端，所以本插件不考虑主动支持旧版
