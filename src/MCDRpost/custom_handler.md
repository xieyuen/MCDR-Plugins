# MCDRpost API--自定义 Handler

一般来说，MCDRpost已经能够适应大多数服务端，但是对于某些特殊情况（比如1.9版本）[^1]，MCDRpost可能无法满足需求，
考虑到插件对 Minecraft 的兼容性，插件暴露了一定的 API 用于 Minecraft 一些特殊服务端的适配

核心 API 有:

- classes
    - [AbstractVersionHandler](#class-abstractversionhandlerabc)
    - [AbstractSoundPlayer](#class-abstractsoundplayerabc)
    - [DefaultVersionHandler](#class-defaultversionhandlerabstractversionhandler)
    - [NewSoundPlayer](#class-newsoundplayerabstractsoundplayer)
    - [OldSoundPlayer](#class-oldsoundplayerabstractsoundplayer)
- functions
    - [register_handler](#function-register_handler)
- types
    - [Item](#class-itemserializable)
    - [Environment](#class-environment)
- constants
    - OFFHAND_CODE

你可以在导入的时候使用下面的方式：

```python
from mcdrpost.api import *
```

当然如果不希望污染全局变量也可以这样：

```python
from mcdrpost import api as mp
```

### class AbstractVersionHandler(ABC)

`AbstractVersionHandler` 是一个抽象类，继承并且实现内部的方法就可以适配你自己的 Minecraft 服务端

> [!NOTE]
> 如果你使用了自定义的 VersionHandler，MCDRpost 总是优先使用你的Handler，
> 除非 Minecraft 版本不支持你的 Handler

#### method replace

|   参数   |   类型   | 描述    |
|:------:|:------:|:------|
| player | `str`  | 玩家 ID |
|  item  | `Item` | 物品信息  |

这个方法需要实现物品替换的命令，参数是玩家的名称和物品的信息

#### method get_offhand_item

|   参数   |   类型   | 描述    |
|:------:|:------:|:------|
| player | `str`  | 玩家 ID |
|  返回值   | `Item` | 物品信息  |

这是 MCDRpost 获取玩家副手物品信息的方法

API 提供了一个常量 `OFFHAND_CODE` 表示副手的位置

#### property play_sound

|        返回值类型        |       描述        |
|:-------------------:|:---------------:|
| AbstractSoundPlayer | 为 MCDRpost 提供音效 |

MCDRpost 通过它播放音效

### class DefaultVersionHandler(AbstractVersionHandler)

这是 MCDRpost 提供的一个对于 `1.17 <= Minecraft 版本 < 1.20.5` 的简单 Handler,

### function register_handler

|   参数    |               类型                | 说明                                         |
|:-------:|:-------------------------------:|:-------------------------------------------|
| handler | `type[AbstractVersionHandler]`  | 要注册的 Handler 类                             |
| checker | `Callable[[Environment], bool]` | 当 checker 返回 True 时 MCDRpost 才会使用此 handler |

当你实现了自定义的 Handler，你需要向 MCDRpost 注册你的 Handler，否则插件不会使用你的 Handler

注意，checker参数是决定 你的 Handler 是否生效的函数，参数是 [Environment](#class-environment) 对象，返回一个布尔值

### class AbstractSoundPlayer(ABC)

这是 MCDRpost 在 3.3.3 版本中添加的 API, 用于播放音效

#### method successfully_receive

|   参数   |  类型   | 描述    |
|:------:|:-----:|:------|
| player | `str` | 玩家 ID |

当玩家成功接收到订单时调用

#### method successfully_post

|    参数    |  类型   | 描述  |
|:--------:|:-----:|:----|
|  sender  | `str` | 寄件人 |
| receiver | `str` | 收件人 |

当玩家成功寄送订单时调用，要给寄件人和收件人两者都播放音效

#### method has_something_to_receive

|   参数   |  类型   | 描述    |
|:------:|:-----:|:------|
| player | `str` | 玩家 ID |

当玩家刚进入服务器且有物品待收时调用

### class NewSoundPlayer(AbstractSoundPlayer)

这是 MCDRpost 为 Minecraft 1.13 及以上版本提供的有效实现

### class OldSoundPlayer(AbstractSoundPlayer)

这是 MCDRpost 为 Minecraft 1.13 以下版本提供的有效实现

### Types

#### class Item(Serializable)

这是 MCDRpost 储存物品信息的数据结构，包含三个属性:

|     属性     |   类型   | 描述                                       |
|:----------:|:------:|:-----------------------------------------|
|     id     | `str`  | 物品的 id, 注意要包括命名空间，比如 `minecraft:diamond` |
|   count    | `int`  | 物品的数量                                    |
| components | `dict` | 物品的 nbt/components 信息                    |

#### class Environment

这里是 MCDRpost 读取的环境信息，当然你也可以通过 Environment._server 获得 PluginServerInterface 实例

|       属性        |         类型         | 描述                                        |
|:---------------:|:------------------:|:------------------------------------------|
| server_version  | `Union[str, None]` | Minecraft 服务器版本，当 MCDR 没有获取到版本信息时为 `None` |
| is_rcon_running |       `bool`       | RCON 是否正在运行                               |
|  mcdr_handler   |       `str`        | MCDR 正在使用的 Handler (相当于服务端的类型)            |

## Example

我们建议使用插件定义你的 Handler，下面是一个单文件插件的例子

```python
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
```

> [!NOTE]
> 在 `on_load()` 函数中定义是为了保证 MCDR 能正确加载插件，
> 因为 MCDR 要先读取 Metadata 才知道插件依赖 MCDRpost，而此时 MCDRpost 不一定已经被加载
> 放在函数中先不运行就可以避免没有优先加载 MCDRpost 导致的问题
>
> **注意：如果是多文件插件就没有这种问题，放在外面定义就好**

如果是用多文件插件的话，你甚至不需要定义 `on_load`, 只需要在入口点内定义 Handler 并注册就好

example_handler/entry.py

```python
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
```

[^1]: 1.13 以前没有 `/data` 命令，要获取玩家物品需要在服务端安装插件，但 MCDR 主打的就是不修改服务端，所以本插件不考虑支持旧版
