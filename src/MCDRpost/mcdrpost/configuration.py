from mcdreforged import Serializable


class CommandPermissions(Serializable):
    """命令权限配置

    MCDR 的权限只有 0, 1, 2, 3, 4 五个等级，
    分别对应的是 ``guest`` ``user`` ``helper`` ``admin`` ``owner`` 五个等级

    Attributes:
        root (int): 根命令权限等级
        post (int): 发送命令权限等级
        receive (int): 收件命令权限等级
        cancel (int): 取消命令权限等级
        list_player (int): 列出玩家命令权限等级
        list_orders (int): 列出订单命令权限等级
        player (int): 玩家命令权限等级
    """

    root: int = 0
    post: int = 0
    receive: int = 0
    cancel: int = 0
    list_player: int = 2
    list_orders: int = 2
    player: int = 3
    reload: int = 3


class PrefixConfig(Serializable):
    enable_addition: bool = True
    more_prefix: list[str] = ["!!post"]


class Configuration(Serializable):
    """插件配置

    Attributes:
        max_storage (int): 每个人发送的订单的最大存储量，-1不限制
        prefix (list[str]): MCDR 命令前缀，可以注册多个作为别名，只需要放在一个列表内即可, !!po 一定会生效
        auto_fix (bool): 是否自动修复无效订单
        auto_register (bool):是否自动为新玩家注册
        receiving_tip_delay (float): 登录之后收件箱提示的延迟时间，单位为秒
        permissions (CommandPermissions): 命令权限配置
    """

    max_storage: int = 5
    prefix: PrefixConfig = PrefixConfig.get_default()
    auto_fix: bool = False
    auto_register: bool = True
    receiving_tip_delay: float = 3
    permissions: CommandPermissions = CommandPermissions.get_default()

    # Deprecated but for compatibility
    command_permission: CommandPermissions = CommandPermissions.get_default()
    allow_alias: bool = True
    command_prefixes: list[str] = ["!!po", "!!post"]
