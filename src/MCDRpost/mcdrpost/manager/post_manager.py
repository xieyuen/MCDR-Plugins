"""
Post 管理器，也是插件核心逻辑处理的地方
"""

from typing import TYPE_CHECKING

from mcdreforged import PluginServerInterface

from mcdrpost.configuration import Configuration
from mcdrpost.data_structure import Item
from mcdrpost.manager.config_manager import ConfigurationManager
from mcdrpost.manager.data_manager import DataManager
from mcdrpost.manager.version_manager import VersionManager
from mcdrpost.service.post_service import PostService
from typing import Literal

if TYPE_CHECKING:
    from mcdrpost.manager.command_manager import CommandManager


class PostManager:
    """Post 管理器，也是插件核心逻辑处理的地方

    Attributes:
        server (PluginServerInterface): MCDR插件接口
        config_manager (ConfigurationManager): 配置管理
        data_manager (DataManager): 订单管理
        command_manager (CommandManager): 命令注册
        version_manager (VersionManager): 版本管理
        post_service (PostService): 邮件服务
    """
    
    # 类变量声明
    server: PluginServerInterface
    config_manager: ConfigurationManager
    data_manager: DataManager
    command_manager: "CommandManager"
    version_manager: VersionManager
    post_service: PostService

    def __init__(self) -> None:
        pass

    @property
    def configuration(self) -> Configuration:
        return self.config_manager.get_configuration()

    # Events Handle
    def on_load(self, server: PluginServerInterface, _prev_module) -> None:
        """事件: 插件加载--在这里会注册插件的命令

        如果服务端已经运行（也就是重新加载插件的情况），会自动地引发服务端启动完成事件
        """
        # 延迟导入以避免循环导入
        from mcdrpost.manager.command_manager import CommandManager
        
        # 初始化所有管理器，并将自身传递给它们
        self.server = server
        self.config_manager = ConfigurationManager(self)
        self.data_manager = DataManager(self)
        self.command_manager = CommandManager(self)
        self.version_manager = VersionManager(server)
        self.post_service = PostService(self)
        self.command_manager.register()
        if server.is_server_running():
            self.on_server_startup(server)

    def on_unload(self, _server: PluginServerInterface) -> None:
        """事件: 插件卸载--保存订单信息"""
        self.data_manager.save()

    def on_player_joined(self, server: PluginServerInterface, player: str, info) -> None:
        """事件: 玩家加入服务器"""
        self.post_service.on_player_joined(server, player, info)

    def on_server_startup(self, _server: PluginServerInterface):
        """事件: 服务器完全开启--刷新游戏版本设置"""
        self.version_manager.refresh()

    def on_server_stop(self, _server: PluginServerInterface, _server_return_code: int):
        """事件: 服务器关闭--保存配置信息和订单信息"""
        self.data_manager.save()

    # 代理方法，保持API兼容性
    def replace(self, player: str, item: Item) -> None:
        """替换玩家的副手物品

        Args:
            player (str): 玩家 id
            item (Item): 要替换的物品
        """
        self.post_service.replace(player, item)

    def check_offhand_empty(self, player: str) -> bool:
        """检查副手物品

        Args:
            player (str): 玩家 id
        """
        return self.post_service.check_offhand_empty(player)

    def get_offhand_item(self, player: str) -> Item | None:
        """获取玩家副手物品

        Args:
            player (str): 玩家 ID
        """
        return self.post_service.get_offhand_item(player)

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID
        """
        return self.post_service.is_storage_full(player)

    def post(self, src, receiver: str, comment: str | None = None) -> None:
        """发送订单

        Args:
            src: 寄件人的相关信息
            receiver (str): 收件人 ID
            comment (str): 备注信息
        """
        self.post_service.post(src, receiver, comment)

    def receive(self, src, order_id: int, typ: str) -> bool:
        """接收订单的物品

        Args:
            src: 命令源
            order_id (int): 被接收的订单的 ID
            typ (str): 类型

        Returns:
            bool: 是否成功接收到物品
        """
        return self.post_service.receive(src, order_id, typ)  # type: ignore

    def reload(self) -> None:
        self.config_manager.reload()
        self.data_manager.reload()