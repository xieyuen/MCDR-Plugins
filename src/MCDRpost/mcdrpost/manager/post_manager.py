import time

from mcdreforged.api.decorator import new_thread
from mcdreforged.api.types import Info, InfoCommandSource, PluginServerInterface

from mcdrpost import constants
from mcdrpost.manager.command_manager import CommandManager
from mcdrpost.manager.config_manager import ConfigurationManager
from mcdrpost.manager.order_manager import OrderManager
from mcdrpost.order_data import OrderInfo
from mcdrpost.utils import get_formatted_item, get_formatted_time, get_offhand_item, play_sound, tr
from mcdrpost.utils.replace_offhand_item import replace_for_17, replace_for_lower_17
from mcdrpost.utils.translation_tags import Tags
from mcdrpost.utils.types import ReplaceFunction


class PostManager:
    """Post 管理器，也是插件核心逻辑处理的地方

    Attributes:
        server (PluginServerInterface): MCDR插件接口
        config_manager (ConfigurationManager): 配置管理
        order_manager (OrderManager): 订单管理
        command_manager (CommandManager): 命令注册
    """

    def __init__(self, server: PluginServerInterface) -> None:
        self.server: PluginServerInterface = server
        self.config_manager: ConfigurationManager = ConfigurationManager(self)
        self.order_manager: OrderManager = OrderManager(self)
        self.command_manager: CommandManager = CommandManager(self)
        self._replace: ReplaceFunction = replace_for_lower_17

    def _refresh_replace(self) -> None:
        if self.config_manager.environment.item_command():
            self._replace: ReplaceFunction = replace_for_17
        else:
            self._replace: ReplaceFunction = replace_for_lower_17

    def replace(self, player: str, item: str) -> None:
        """替换副手物品

        Args:
            player (str): 玩家名
            item (str): 要替换的物品 id
        """
        self._replace(self.server, player, item)

    def on_load(self, _server: PluginServerInterface, _prev_module) -> None:
        """事件: 插件加载--在这里会注册插件的命令

        .. note::
            PostManager在插件导入时通过 ``PluginServerInterface.psi()`` 获取到 PluginServerInterface 实例进行实例化，
                而非一般的在 on_load() 内得到 PluginServerInterface 实例再实例化
        """
        self.command_manager.register()

    def on_unload(self, _server: PluginServerInterface) -> None:
        """事件: 插件卸载--保存配置文件和订单信息"""
        self.config_manager.save()
        self.order_manager.save()

    def on_player_joined(self, server: PluginServerInterface, player: str, _info: Info) -> None:
        """事件: 玩家加入服务器

        由于 MCDRpost 不支持向未注册的玩家发送物品，要注册也不能让腐竹一个个加
        我们会在玩家加入的时候自动注册，对于老玩家，如果有未接收的订单我们会推送消息
        """
        if not self.order_manager.is_player_registered(player):
            # 还未注册的玩家
            self.order_manager.add_player(player)
            server.logger.info(tr(Tags.login_log, player))
            self.order_manager.save()
            return

        # 已注册的玩家，向他推送订单消息（如果有）
        if self.order_manager.has_unreceived_order(player):
            @new_thread('MCDRpost-send receive tip')
            def send_receive_tip():
                time.sleep(self.config_manager.configuration.receive_tip_delay)
                server.tell(player, tr(Tags.wait_for_receive))
                play_sound.has_something_to_receive(server, player)

            send_receive_tip()

    def on_server_startup(self, _server: PluginServerInterface):
        self._refresh_replace()

    def on_server_stop(self, _server: PluginServerInterface, _server_return_code: int):
        """事件: 服务器关闭--保存配置信息和订单信息"""
        self.save()

    def is_storage_full(self, player: str) -> bool:
        """玩家发送的订单是否抵达上限

        Args:
            player (str): 玩家 ID
        """
        if self.config_manager.configuration.max_storage == -1:
            return False
        return len(self.order_manager.get_orders_by_sender(player)) >= self.config_manager.configuration.max_storage

    def post(self, src: InfoCommandSource, receiver: str, comment: str = None) -> None:
        """发送订单

        Args:
            src (InfoCommandSource): 寄件人的相关信息
            receiver (str): 收件人 ID
            comment (str): 备注信息
        """
        sender = src.get_info().player

        if self.is_storage_full(sender):
            src.reply(tr(Tags.at_max_storage, self.config_manager.configuration.max_storage))
            return

        if sender == receiver:
            src.reply(tr(Tags.same_person))
            return

        if comment is None:
            comment = tr(Tags.no_comment)

        item = get_formatted_item(
            get_offhand_item(self.server, sender)
        )

        # create order
        order_id = self.order_manager.add_order(OrderInfo(
            sender=sender,
            receiver=receiver,
            item=item,
            comment=comment,
            time=get_formatted_time(),
        ))

        self.replace(sender, constants.AIR)
        src.reply(tr(Tags.reply_success_post))
        self.server.tell(receiver, tr(Tags.hint_receive, order_id))
        play_sound.successfully_post(self.server, sender, receiver)
        self.order_manager.save()

    def receive(self, src: InfoCommandSource, order_id: int):
        """接收订单

        Args:
            src (InfoCommandSource): 收件人的相关信息
            order_id (int): 被接收的订单的 ID
        """
        player = src.get_info().player

        # 订单接收者不是 TA
        if order_id not in self.order_manager.get_orders_by_receiver(player):
            src.reply(tr(Tags.unchecked_orderid))
            return

        # 副手有东西 拒绝接收
        if get_offhand_item(self.server, player):
            src.reply(tr(Tags.clear_offhand))
            return

        order = self.order_manager.pop_order(order_id)
        self.replace(player, order.item)
        play_sound.receive(self.server, player)

    def save(self):
        self.config_manager.save()
        self.order_manager.save()

    def reload(self):
        self.config_manager.reload()
        self.order_manager.reload()


__all__ = ['PostManager']
