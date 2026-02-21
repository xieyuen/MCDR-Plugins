# KillServer

在关服卡死时强制关闭服务器

> [!WARNING]
> 此插件使用 [dowhen](http://github.com/gaogaotiantian/dowhen/) 模块实现, 可能不够稳定

## 介绍

对于下面的两种情况(实际可能还有更多适用的情况):

1. Fabric 服务器卡死不关闭
   - [MCDReforged/MCDReforged#150](https://github.com/MCDReforged/MCDReforged/issues/150)
   - [EngineHub/WorldEdit#2459](https://github.com/EngineHub/WorldEdit/issues/2459)
2. `pause` 命令诱发用户Ctrl+C操作，导致 MCDR 关闭与存档恢复冲突，最终致使存档损坏
   - [TISUnion/PrimeBackup#85](https://github.com/TISUnion/PrimeBackup/issues/85)
   - [MCDReforged/MCDReforged#394](https://github.com/MCDReforged/MCDReforged/issues/394)

本插件提供监听服务器关闭并且在这些情况下强制关闭服务器的功能, 给小白腐竹们提供一个简单且无脑的解决方案

## 配置

|      配置项       |   类型    |  默认值   | 含义                 | 注释      |
|:--------------:|:-------:|:------:|:-------------------|:--------|
|    `enable`    | `bool`  | `True` | 是否启用插件             | 不影响事件分发 |
| `waiting_time` | `float` |  `60`  | 等待服务器关闭的时间, 超时强制关闭 | 单位为秒    |

## 使用方法

直接安装到 MCDR 的插件文件夹下即可, 可以从 [GitHub](https://github/xieyuen/MCDR-Plugins)
或 [PluginCatalogue](https://mcdreforged.com/zh-CN/plugin/kill_server) 手动下载插件文件

你也可以用下面的 MCDR 命令安装 KillServer

```mcdr
!!MCDR plg install kill_server
```

安装后只需要注意服务器关闭不要用 Minecraft 原生的 `/stop` 命令, 换用 MCDR 命令来关闭,
比如 `!!MCDR server stop` `!!MCDR server restart`

> 你都用 MCDR 了竟然还不知道原生 `/stop` 会让 MCDR 关闭吗?<br>
> 你都用 MCDR 了竟然还用不支持运行时回档的备份模组而不是 PrimeBackup、QuickBackupM 吗?

## 新的事件

KillServer 创建了三个字面量事件 [`ServerStoppingEvent`](#serverstoppingevent),
[`PluginStoppingServerEvent`](#pluginstoppingserverevent)
和 [`WorldSavedEvent`](#worldsavedevent)

```python
from kill_server import ServerStoppingEvent, PluginStoppingServerEvent, WorldSavedEvent
```

### ServerStoppingEvent

KillServer 创建了一个字面量事件 `ServerStoppingEvent = LiteralEvent("kill_server.server_stopping")`
用以监听服务器关闭, 这个事件会在服务器关闭时 (例如 `/stop` 被调用时) 触发

- **事件 ID**: `kill_server.server_stopping`
- **回调参数**: `PluginServerInterface`

### PluginStoppingServerEvent

KillServer 创建了一个字面量事件 `PluginStoppingServerEvent = LiteralEvent("kill_server.plugin_stopping_server")`
用以监听 ***由插件调用 `ServerInterface.stop()` 或调用 MCDR 命令*** 导致的服务器关闭,
这个事件会在服务器关闭时 (例如 `!!MCDR server stop` 被调用时) 触发

> [!IMPORTANT]
> 1. 该事件同时会引发 [`ServerStoppingEvent`](#serverstoppingevent)
> 2. `ServerInterface.kill()` 不会触发该事件, 因为服务器此时不是正常关闭

- **事件 ID**: `kill_server.plugin_stopping_server`
- **回调参数**: `PluginServerInterface`

### WorldSavedEvent

KillServer 创建了一个字面量事件 `WorldSavedEvent = LiteralEvent("kill_server.world_saved")`
用以监听服务器是否将世界保存好, 这个事件会在服务器保存世界完成时 (例如 `/save` 被调用之后) 触发

- **事件 ID**: `kill_server.world_saved`
- **回调参数**: `PluginServerInterface`

> [!TIP]
> 如果你只是需要各个事件而不需要强制关闭功能的话可以把配置中的 `enable` 项设定为 `false`,
> 该配置只会影响强制关闭功能而不会停止事件分发
