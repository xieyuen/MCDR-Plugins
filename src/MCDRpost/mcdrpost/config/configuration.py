from mcdreforged.api.utils import Serializable


class CommandPermission(Serializable):
    """命令权限配置

    MCDR 的权限只有 0, 1, 2, 3, 4 五个等级
    分别对应的是 ``guest`` ``user`` ``helper`` ``admin`` ``owner`` 五个等级
    这些都是 MCDR 合法的权限

    Attributes:
        root (int): 根命令权限等级
        post (int): 发送命令权限等级
        receive (int): 收件命令权限等级
        cancel (int): 取消命令权限等级
        list_player (int): 列出玩家命令权限等级
        list_orders (int): 列出订单命令权限等级
        player (int): 玩家命令权限等级
        save (int): 保存命令权限等级
        reload (int): 重载命令权限等级
    """
    root: int = 0
    post: int = 0
    receive: int = 0
    cancel: int = 0
    list_player: int = 2
    list_orders: int = 2
    player: int = 3
    save: int = 3
    reload: int = 3


class Configuration(Serializable):
    """插件配置

    Attributes:
        max_storage (int): 每个人发送的订单的最大存储量，-1不限制
        allow_alias (bool): 是否允许命令别名，如果为 False,则只会注册 !!po
        command_prefixes (list[str]): MCDR 命令前缀，可以注册多个作为别名，只需要放在一个列表内即可, !!po 一定会生效
        auto_fix (bool): 是否自动修复无效订单
        receive_tip_delay (float): 登录之后收件箱提示的延迟时间，单位为秒
        command_permission (CommandPermission): 命令权限配置
    """
    max_storage: int = 5
    allow_alias: bool = True
    command_prefixes: list[str] = ['!!po', "!!post"]
    auto_fix: bool = False
    receive_tip_delay: float = 3
    command_permission: CommandPermission = CommandPermission()


__all__ = ['Configuration']
