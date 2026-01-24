# MCDRpost

## 版权信息

- 原作者: [Flyky](https://github.com/Flyky)
- 原仓库: [MCDRpost](https://github.com/Flyky/MCDRpost)
- 现维护者/开发者: [xieyuen](https://github.com/xieyuen)
- LICENSE: [GPL 3.0](../../LICENSE)

## 一些更新信息

> [!WARNING]
> 1. 插件的 `2.x` 版本已经停止更新，并且不支持 Minecraft 1.20.5 或者更高版本[^1]
> 2. 插件的 `3.x` 版本与旧版（`2.x`）不兼容，升级新版本建议清空中转站或者手动改变数据结构
> 3. 在 `3.4.0` 版本之前, 本插件不支持使用[新版本号命名规则](<https://www.minecraft.net/en-us/article/minecraft-new-version-numbering-system>)的 Minecraft

*Added on 2025 6th Sept.*: 已经实现了旧版本数据文件的自动升级转换，
见 [README](<../MCDRpost-migration/README.md>) 或者 [release](https://github.com/xieyuen/MCDR-Plugins/releases/tag/mcdrpost-migration)

- 如果直接加载新版本，旧版的订单数据不能被加载，但是原来的数据仍然存在，并且会创建一个新的空文件 `orders.json` 来存储订单数据

更新日志见 [CHANGELOG](CHANGELOG.md)

## 介绍

一个用于邮寄/传送物品的MCDR插件

[-> MCDReforged <-](https://github.com/Fallen-Breath/MCDReforged)

![MCDRpost help](https://s1.ax1x.com/2020/04/16/Jk8ysP.png)

## 依赖

- Python >= 3.10
- MCDReforged >= 2.15.0
- [Minecraft Data API](https://github.com/MCDReforged/MinecraftDataAPI) 任意版本
- Minecraft >= 1.13 (如果不使用自定义 Handler)[^2]

> [!IMPORTANT]
> 我们十分推荐开启服务器的 RCON

## 安装

将在 release 或 catalogue 下载的 `.mcdr` 插件文件放入插件目录下加载即可

> [!NOTE]
>
> 在MCDR中，可以直接使用
>
> ```
> !!MCDR plugin install mcdrpost
> ```
>
> 来安装 MCDRpost, 这也是推荐做法

## 功能

**使用该插件可以将副手的物品发送给别的玩家**  
也可以发送给离线玩家（但该玩家必须曾经进过服务器）  
*不可以发送给自己哦~*

- 玩家发出物品后，物品(订单)将会存放在【中转站】
- 需要收件人收取订单才能收到物品，之后【中转站】会删除该订单
- 还未查收的订单可以取消，物品会从【中转站】退回，并删除订单
- 每人存放【中转站】的订单数有上限，以防止把邮件寄送作为储存箱等的滥用
- 如果你要问为啥一定是用副手传送接收呢 ，因为
    - 用 `give` 传到身上任意栏位，如果身上东西多的话，传回来还要找一下，比较麻烦，还不容易找到传回来的是哪个东西
    - 如果身上东西满了的话 `give` 是拿不到物品的，防止粗心大意的小天才
    - 该插件传送和接收前均会检查并提示副手物品，不用担心会直接 replace 掉原本副手的物品
    - 当然为什么不传送当前主手所持栏位进行传送呢？ ~~因为懒2333~~

## 使用

|              命令(全写)              |             缩写              | 说明                                |
|:--------------------------------:|:---------------------------:|:----------------------------------|
|             `!!post`             |           `!!po`            | 显示帮助信息, 所有的 `!!post` 都可以换成 `!!po` |
| `!!post post <player> [comment]` | `!!po p <player> [comment]` | 发送副手物品，可以没有备注                     |
|    `!!post receive <orderid>`    |     `!!po r <orderid>`      | 接收输入单号的物品到副手                      |
|    `!!post cancel <orderid>`     |     `!!po c <orderid>`      | 取消订单，仅限对方未收取时                     |
|        `!!post post_list`        |          `!!po pl`          | 列出发件列表                            |
|        `!!post list post`        |       `!!po ls post`        | 列出发件列表                            |
|      `!!post receive_list`       |          `!!po rl`          | 列出收件列表                            |
|      `!!post list receive`       |      `!!po ls receive`      | 列出收件列表                            |
|      `!!post list players`       |      `!!po ls players`      | 列出已注册玩家名单                         |
|   `!!post player add <player>`   |                             | 注册一个新玩家                           |
| `!!post player remove <player>`  |                             | 删除已经注册的玩家                         |

*上面命令中的`r`表示`receive`，`p`表示`post`，`l`表示`list`，`c`表示`cancel`*

*Added in version 3.1.0:* 支持命令的全写，例如`!!po post Flyky full-name-support`

*Added in version 3.1.0:* `list` 子命令新增 `post` `receive`，效果等同于 `!!po pl` 和 `!!po rl`

## 配置

MCDRpost的配置文件（3.0.0或以上）在 `config/MCDRpost/config.yml` 中  
但是旧版本（2.1.1或以下）没有配置文件，请自行修改插件中的 `mcdrpost/__init__.py`

**点击快速跳转**

- [2.x](#211-及以下)
- [3.x](#300-版本或以上)

### 2.1.1 及以下

> [!NOTE]
> 该版本已归档, 不再维护, 推荐使用新版本

对于 2.1.1 及以下的版本(应该说，2.1.0 和 2.1.1)，**Flyky 并没有提供配置文件**，想要配置需要编辑 `mcdrpost/__init__.py` 才能够修改

在 `mcdrpost/__init__.py` 文件中 Line 13 ~ 17，有以下五行代码

```python
Prefix = '!!po'
MaxStorageNum = 5  # 最大存储订单量，设为-1则无限制
SaveDelay = 1
OrderJsonDirectory = './config/MCDRpost/'
OrderJsonFile = OrderJsonDirectory + 'PostOrders.json'
```

这些属性就是配置，含义见下表

|         属性         |  类型   |                  默认值                  | 描述                        |
|:------------------:|:-----:|:-------------------------------------:|:--------------------------|
|       Prefix       | `str` |               `'!!po'`                | 插件命令的前缀                   |
|   MaxStorageNum    | `int` |                  `5`                  | 每个玩家最大存储的订单数量，-1 不限制      |
|     SaveDelay      | `int` |                  `1`                  | 新增 `SaveDelay` 个订单时保存一次   |
| OrderJsonDirectory | `str` |        `'./config/MCDRpost/'`         | 订单数据文件储存的文件夹              |
|   OrderJsonFile    | `str` | `'./config/MCDRpost/PostOrders.json'` | 订单数据文件的名称，应是一个 `.json` 文件 |

> [!NOTE]
> Line 18 处的 `command_item = -2` 请别动，这是用来自动检测版本的

### 3.0.0 版本或以上

在 3.0.0 版本中, [xieyuen](https://github.com/xieyuen) 对插件进行了模块化重构，
配置不再是写死在代码中，而是放到了配置文件 `config.yml` 中

下面的 [配置表](#配置表) 是最新版本配置文件的内容

#### 配置表

|           属性           |  Python类型   |         默认值          | 描述                 | 备注             |
|:----------------------:|:-----------:|:--------------------:|:-------------------|:---------------|
|      allow_alias       |   `bool`    |        `true`        | 是否允许别名             | 已弃用[^3]        |
|        auto_fix        |   `bool`    |       `false`        | 是否自动修复订单           |                |
|     auto_register      |   `bool`    |        `true`        | 是否自动为新玩家注册         |                |
|      max_storage       |    `int`    |         `5`          | 订单最大存储量，设置为 -1 不限制 |                |
|   receive_tip_delay    |   `float`   |        `3.0`         | 提示延迟               |                |
|    command_prefixes    | `list[str]` | `['!!po', '!!post']` | 命令根节点              | 已弃用[^3]        |
|   command_permission   |   `dict`    |          ~           | 见[权限表](#权限表)       | 已弃用[^3]        |
| prefix.enable_addition |   `bool`    |        `true`        | 是否注册多个根命令          | 代替 allow_alias |
|   prefix.more_prefix   |   `bool`    |        `true`        | 是否注册多个根命令          | 代替 allow_alias |

> [!NOTE]
> `allow_alias` `command_prefixed` 已经弃用并被合并到 `prefix` 内

#### 权限表

> [!NOTE]
> MCDReforged 的权限系统支持 5 种权限: 
> `owner`, `admin`, `helper`, `user`, `guest`,
> 在设定权限的时候，用 0~4 五个数字代替权限等级
>
>> 更多权限信息见 [MCDR 官方文档](https://docs.mcdreforged.com/zh-cn/latest/permission.html#overview)

|      属性      | 默认权限 | 描述                     |
|:------------:|:----:|:-----------------------|
|     root     |  0   | 根命令的权限                 |
|     post     |  0   | 发送邮件的权限(同时包括列出发件列表的权限) |
|   receive    |  0   | 接收邮件的权限(同时包括列出收件列表的权限) |
|    cancel    |  0   | 取消邮件的权限                |
| list_orders  |  2   | 获得中转站全部订单信息的权限         |
| list_players |  2   | 获得全部已注册玩家的权限           |
|    player    |  3   | `player` 子命令的权限        |

[配置文件 demo](https://gist.github.com/xieyuen/36f3c272d05b59ac6d0fe9e8a690b312)

## 注意信息

- 可能会有部分带有特殊复杂NBT标签的物品无法传送，会提示检测不到可传送的物品，所以尝试一下即可
- 不开启 RCON 的话，插件可能会有一定的延迟导致发送/接收失败

> [!WARNING]
> ***切勿传送原版非法堆叠数的物品!!!***
> 
> 例如使用carpet地毯堆叠的空潜影盒，会导致该物品无法接收
> 
> ~~[自定义 Handler](#api) + 特定模组兼容 也许可以解决这个问题~~

> [!IMPORTANT]
> 如果您的 Minecraft 服务器要从 1.20.5 以下升级到 1.20.5 版本或以上，请让玩家们清空中转站，
> 因为订单数据的 nbt 不能自动地转化成新版本的 components，升级之后订单的物品会因为标签结构改变而不能取走

## 一些图片

![po rl](https://s1.ax1x.com/2020/04/16/Jk0WnJ.png)

![po r](https://s1.ax1x.com/2020/04/16/Jk0fB9.png)

![po p](https://s1.ax1x.com/2020/04/16/Jk02X4.png)

## API

> [!NOTE]
> 如果你在使用插件的时候没有遇到什么问题，可以忽略这段内容

点击 [此处](custom_handler.md) 跳转至 MCDRpost 的自定义 Handler 文档

## Future

在将来某一个时间（也许是 MCDR 不再支持 Python 3.10 的时候），
MCDRpost 将会从 Python 3.10 迁移到 3.12 或者更高版本，届时 MCDRpost 将会进入 4.x 版本

<!--
[这里](https://github.com/xieyuen/MCDR-Plugins/tree/dev/MCDRpost-3.12/src/MCDRpost) 是 Python 3.12+ 的特别版本
-->

[^1]: Minecraft 1.20.5 用 components 代替了 tag，导致命令不能执行，Minecraft 报错见 Flyky/MCDRpost#10
[^2]: 理论上使用自定义 Handler 就可以适配任何版本，但是插件**本身没有兼容**低于 1.13 的版本，原因见 [Custom Handler](custom_handler.md)
[^3]: 该属性/配置项已经在 v3.4.0 中被弃用，将在 v3.6 中被删除
