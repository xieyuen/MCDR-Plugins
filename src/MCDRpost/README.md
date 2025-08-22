# MCDRpost

## Original Author

- 原作者: [Flyky](https://github.com/Flyky)
- 原仓库: [MCDRpost](https://github.com/Flyky/MCDRpost)

## Introduce

A MCDR plugin for post/teleport items  
一个用于邮寄/传送物品的MCDR插件

[-> MCDReforged <-](https://github.com/Fallen-Breath/MCDReforged)

![MCDRpost help](https://s1.ax1x.com/2020/04/16/Jk8ysP.png)

# Install

将在 release 下载的 `.mcdr` 插件文件放入插件目录下重载插件即可  
**当前必须使用Rcon获取信息，请一定配置好服务器和MCDR的Rcon**  
*MCDRpost(ver1.0.0+)依赖[Minecraft Data API插件](https://github.com/MCDReforged/MinecraftDataAPI)
，请先安装[Minecraft Data API插件](https://github.com/MCDReforged/MinecraftDataAPI)*  
~~*旧版本依赖[PlayerInfoAPI插件](https://github.com/TISUnion/PlayerInfoAPI)*~~

在MPM弃用之后的MCDR中，可以直接使用

```text
!!MCDR plg install mcdrpost
!!MCDR confirm
```

来安装 2.1.0 版本的 MCDRpost

> 我还没有与Fallen和Flyky取得联系，仓库内的新版本的更新暂不支持自动下载

# Feature

**使用该插件可以将副手的物品发送给别的玩家**  
也可以发送给离线玩家（但该玩家必须曾经进过服务器）  
*不可以发送给自己哦~*

- 玩家发出物品后，物品(订单)将会存放在【中转站】
- 需要收件人收取订单才能收到物品，之后【中转站】会删除该订单
- 还未查收的订单可以取消，物品会从【中转站】退回，并删除订单
- 每人存放【中转站】的订单数有上限（防止作为储存箱等的滥用），默认为 5[^1]
- 如果你要问为啥一定是副手用 `replaceitem` 传送接收呢 ，因为
    - 用 `give` 传到身上任意栏位，如果身上东西多的话，传回来还要找一下，比较麻烦，还不容易找到传回来的是哪个东西
    - 如果身上东西满了的话 `give` 是拿不到物品的，防止粗心大意的小天才
    - 该插件传送和接收前均会检查并提示副手物品，不用担心会直接replace掉原本副手的物品
    - 当然为什么不传送当前主手所持栏位进行传送呢？ 因为我懒2333
    - minecraft ver1.17之后移除了`replaceitem`命令，改为了`item replace`

## Usage

- `!!po` 显示帮助信息
- `!!po p [收件人id] [备注]` 将副手物品发送给[收件人]，[备注]为可选项
- `!!po rl` 列出收件列表。包括[发件人]，[寄件时间]，[备注消息]和[单号]
- `!!po r [单号]` 确认收取该单号的物品到副手(收取前将副手清空)
- `!!po pl` 列出发件(待收取)列表，包括[收件人]，[寄件时间]，[备注消息]和[单号]
- `!!po c [单号]` 取消传送物品(收件人还未收件前)，该单号物品退回到副手(取消前将副手清空)
- `!!po ls players` 查看可被寄送的注册玩家列表
- `!!po ls orders` 查看当前中转站内所有订单 [helper以上权限可用]
- `!!po player add [玩家id]` 手动注册玩家到可寄送玩家列表 [admin以上权限可用]
- `!!po player remove [玩家id]` 删除某注册的玩家 [admin以上权限可用]

*上面命令中的`r`表示`receive`，`p`表示`post`，`l`表示`list`，`c`表示`cancel`*

*Added in version 3.1.0:* 支持命令的全写，例如`!!post post Flyky full-name-support` `list`

*Added in version 3.1.0:* `list` 子命令新增 `post` `receive`，等同于 `pl` 和 `rl`

## Configurations

MCDRpost的配置文件（限v3.0.0或以上）在 `config/MCDRpost/config.yml` 中
但是旧版本（2.1.1或以下）没有配置文件，请自行修改插件中的 `mcdrpost/__init__.py`，详细配置如下

### 2.1.1 及以下

对于 2.1.1 及以下的版本，**Flyky并没有提供配置文件**，想要配置需要编辑 `mcdrpost/__init__.py` 才能够修改

在 `mcdrpost/__init__.py` 文件中 Line 13~17，有以下五行代码

```python
Prefix = '!!po'
MaxStorageNum = 5  # 最大存储订单量，设为-1则无限制
SaveDelay = 1
OrderJsonDirectory = './config/MCDRpost/'
OrderJsonFile = OrderJsonDirectory + 'PostOrders.json'
```

各个属性的含义如下：

- `Prefix`
    - 这是插件命令的前缀，接收一个 `str`
    - 默认为 `!!po`
- `MaxStorageNum`
    - 每个人的最大订单存储数量，接收一个 `int`，设定为 -1 则无限制
    - 默认为 5
- `SaveDelay`
    - 保存间隔，也就是在新增 `SaveDelay` 个订单时保存一次，接收一个 `int`
    - 默认为 1
- `OrderJsonDirectory`
    - 订单数据文件储存的文件夹，应是一个写着有效路径 `str`
    - 默认为 `'./config/MCDRpost/'`
- `OrderJsonFile`
    - 订单数据文件的名称，应是一个 `.json` 文件

### 3.0.0 版本或以上

在 3.0.0 和 3.1.0 版本中，@xieyuen 对插件进行了模块化重构，配置不再是写死在代码中，而是放到了配置文件 `config.yml` 中

以下是配置文件的内容，[点此查看默认配置文件](<demo/config.yml>)

- allow_alias
    - 是否启用命令别名，关闭后 `command_prefixes` 的配置将会作废，锁定为 `!!po`
    - 类型: `bool`
    - 默认值: `true`
- auto_fix
    - 是否自动修复订单
    - 类型: `bool`
    - 默认值: `false`
- auto_register
    - 是否自动为新玩家注册
    - 类型: `bool`
    - 默认值: `true`
- max_storage
    - 订单的最大存储量
    - 类型: `int`
    - 默认值: `5`
- command_prefixes
    - 命令的根节点
    - 类型: `list[str]`
    - 默认值: `["!!po", "!!post"]`
- command_permission
    - 命令权限，下面的配置都是 `Literal[0, 1, 2, 3, 4]` 类型，超出范围的MCDR会报错
    - 配置:
        - root
            - 根命令权限
            - 默认值: 0
        - post
            - 发送邮件(`!!po p`)的权限，同时包括列出自己发出的邮件的权限(`!!po pl`)
            - 默认值: 0
        - receive
            - 接收邮件(`!!po r`)的权限，同时包括列出自己未收取的邮件的权限(`!!po rl`)
            - 默认值: 0
        - cancel
            - 取消邮件(`!!po c`)的权限
            - 默认值: 0
        - list_player
            - 列出已注册玩家的权限
            - 默认值: 2
        - list_orders
            - 列出所有邮件的权限
            - 默认值: 2
        - player
            - 子命令 `player` 的权限
            - 默认值: 3
        - save
            - 保存配置和订单数据
            - 默认值: 3
        - reload
            - 重载配置和订单数据
            - 默认值: 3

## ATTENTIONS!!

- 可能会有部分带有特殊复杂NBT标签的物品无法传送，会提示检测不到可传送的物品，所以尝试一下即可
- **切勿传送原版非法堆叠数的物品**，例如使用carpet地毯堆叠的空潜影盒，会导致该物品无法接收

## known issues

1. ~~因引用的`PlayerInfoAPI插件`在查询不到数据时的默认响应时间timeout较长，即在收寄时的检测副手为空的响应时间较长  ~~
   ~~所以在收寄过程时可能需要稍作等待~~
   **~~但服务器开启并设置好MCDR可连接的rcon则不会出现此问题~~**~~，所以墙裂建议配置rcon~~
    - 目前 `PlayerInfoAPI` 已经弃用，`MCDRpost` 改用`MinecraftDataAPI`
2. **必须使用Rcon获取信息，请一定配置好服务器和MCDR的Rcon**

# pics

![po rl](https://s1.ax1x.com/2020/04/16/Jk0WnJ.png)  
![po r](https://s1.ax1x.com/2020/04/16/Jk0fB9.png)  
![po p](https://s1.ax1x.com/2020/04/16/Jk02X4.png)  
