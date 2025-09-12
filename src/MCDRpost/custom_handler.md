# MCDRpost API

一般来说，MCDRpost已经能够适应大多数服务端，但是对于某些特殊情况，MCDRpost可能无法满足需求，
考虑到插件对 Minecraft 的兼容性，插件暴露了一定的 API 用于 Minecraft 一些特殊服务端的适配

### AbstractVersionHandler(ABC)

`AbstractVersionHandler` 是一个抽象类，继承并且实现内部的方法就可以适配你自己的 Minecraft 服务端

> [!NOTE]
> 如果你使用了自定义的 VersionHandler，MCDRpost 总是优先使用你的Handler，
> 除非 Minecraft 版本不支持你的 Handler

#### method item2str(self, item: Item) -> str:

这个方法需要把 `Item` 对象转换为 `str`，
参数是物品的信息，应该返回一个物品字符串，例如：

物品 附魔耐久3的钻石剑
`Item(id="minecraft:diamond_sword", count=1, components={"minecraft:enchantments": {"levels": {"minecraft:unbreaking": 3}}})`
应该被翻译为（如果是原版 1.20.5 或以上的服务端）
`'minecraft:diamond_sword[minecraft:enchantments={"levels":{"minecraft:unbreaking": 3}}]'`

#### method dict2item(self, item: dict) -> Item:

这个方法是把物品信息转换成 Item 对象，
其中物品信息是一个由 Minecraft 服务端的 `/data get` 命令得到的一个字典

#### method replace(self, player: str, item: str) -> None:

这个方法需要实现物品替换的命令，参数是玩家的名称和物品的信息，
物品信息是由 [item2str](#method-item2strself-item-item---str) 方法生成的字符串

### function register_handler(handler: type[AbstractVersionHandler], checker: Callable[[Environment], bool])

当你实现了自定义的 Handler，你需要向 MCDRpost 注册你的 Handler，否则插件不会使用你的 Handler

注意，checker参数是决定 你的 Handler 是否生效的函数，参数是 [Environment](#class-environment) 对象，返回一个布尔值

### Type Annotations

#### class Item(Serializable)

这是 MCDRpost 储存物品信息的数据结构，包含三个属性:

1. id
    - 物品的 id, 注意要包括命名空间，比如 `minecraft:diamond`
    - type: `str`
2. count
    - 物品的数量
    - type: `int`
3. components
    - 物品的 nbt/components 信息，这应该是一个 python 字典
    - type: `dict

#### class Environment

这里是 MCDRpost 读取的环境信息，当然你也可以通过 Environment._server 获得 PluginServerInterface 实例

##### property sever_version

Minecraft 服务端版本号