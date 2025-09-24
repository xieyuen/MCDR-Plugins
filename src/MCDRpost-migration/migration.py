import json
import os.path
import re
from datetime import datetime
from typing import Any, Callable, Literal, TypeAlias

from mcdreforged import Serializable


class Item(Serializable):
    id: str
    count: int
    components: dict


class Order(Serializable):
    id: int
    time: str
    sender: str
    receiver: str
    comment: str
    item: Item


class NewOrderData(Serializable):
    players: list[str] = []
    orders: dict[str, Order] = {}


AIR = Item(id='minecraft:air', count=1, components={})

LEVELS: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class SimpleLogger:

    def __init__(self):
        self.format_str = '[{time}] [{level}] {msg}'

    def __enter__(self):
        self.log_file = open("migration.log", "w")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log_file.close()

    def _log(self, msg: str, level: LEVELS):
        text = self.format_str.format(time=datetime.now(), level=level, msg=msg)
        print(text)
        if hasattr(self, "log_file"):
            self.log_file.write(text + '\n')
            self.log_file.flush()

    def info(self, msg: str):
        self._log(msg, "INFO")

    def warning(self, msg: str):
        self._log(msg, "WARNING")

    def error(self, msg: str):
        self._log(msg, "ERROR")

    def catch(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.error(f"An error occurred: {e}")
                raise

        return wrapper


logger = SimpleLogger()


class OldOrdersData:
    def __init__(self, data_file_path: str):
        self.players = []
        self.ids = []
        self.orders = {}
        self.json_file_path = data_file_path

    def load_json(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            orders_dict = json.load(f)
            self.players = orders_dict.get('players', [])
            self.ids = orders_dict.get('ids', [])
            self.orders = orders_dict
            self.orders.pop('players')
            self.orders.pop('ids')


def is_in_mcdr_dir() -> bool:
    """判断当前目录是否为 MCDR 服务器的根目录"""
    return os.path.exists('config.yml') and os.path.exists('permission.yml')


def fix_nbt_format(nbt_content: str) -> str:
    """修复 NBT 格式使其符合JSON规范。"""
    if not nbt_content:
        return "{}"

    # 先处理原始字符串，修复一些常见的格式问题
    fixed = nbt_content

    # 修复数字和单位之间有空格的情况，如 "lvl: 3 s" -> "lvl: \"3s\""
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*([,}])', r':\1\3', fixed)
    # 修复键值对之间的空格问题，如 "lvl: 3 s,id:" -> "lvl: \"3s\",id:"
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*,', r':"\1\2",', fixed)
    # 处理数组中的对象，修复其中的格式问题
    fixed = re.sub(r'\[\s*{', '[{', fixed)
    fixed = re.sub(r'}\s*]', '}]', fixed)
    # 修复未加引号的键（确保键名被双引号包围）
    fixed = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', fixed)
    # 处理开头的键（没有前导字符的情况）
    fixed = re.sub(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', fixed)
    # 修复布尔值
    fixed = re.sub(r':\s*(true|false)\s*([,}])', r':"\1"\2', fixed)
    # 修复数字后缀 (再次处理，确保覆盖所有情况)
    fixed = re.sub(r':\s*(\d+)([bslfd])\s*([,}])', r':"\1\2"\3', fixed)
    # 确保字符串有引号
    fixed = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,}])', r':"\1"\2', fixed)
    # 修复数组中的字符串
    fixed = re.sub(r'\[\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*]', r'["\1"]', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*,', r',"\1",', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*]', r',"\1"]', fixed)

    # 确保所有内容都被大括号包围
    if not fixed.startswith('{'):
        fixed = '{' + fixed
    if not fixed.endswith('}'):
        fixed = fixed + '}'

    return fixed


def parse_nbt_content(nbt_content: str) -> dict:
    """解析 NBT 内容为字典。"""
    if not nbt_content:
        return {}

    try:
        # 首先尝试直接解析
        return json.loads(f"{{{nbt_content}}}")
    except json.JSONDecodeError:
        try:
            # 如果失败，则尝试修复格式
            fixed_nbt = fix_nbt_format(nbt_content)
            return json.loads(fixed_nbt)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON解析错误: {e}")
            return {"raw_nbt": nbt_content}


def parse_item(item_string: str) -> tuple[int, str, str, dict[str, Any]] | None:
    """解析 Minecraft 物品字符串

    该函数能够解析 Minecraft 的 /give 命令中使用的物品字符串格式，支持模组物品
    并将 NBT 标签转换为 Python 字典格式。

    Args:
        item_string: Minecraft物品字符串，格式如：
            - 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3, id: "minecraft:unbreaking"}]}'
            - 'create:wrench{Unbreakable: 1b} 3'
            - 'minecraft:apple 64'
            - 'botania:mana_tablet'

    Returns:
        包含四个元素的元组，格式为 (数量, 命名空间, 物品ID, NBT字典)，
        如果解析失败则返回None。

        - 数量 (int): 物品的数量，默认为1
        - 命名空间 (str): 物品的命名空间，如 'minecraft', 'create' 等
        - 物品ID (str): 物品的ID，如 'diamond_pickaxe', 'wrench' 等
        - NBT字典 (dict[str, Any]): NBT标签解析后的字典，如果没有NBT则为空字典

    Examples:
        >>> parse_item('minecraft:diamond_pickaxe{Enchantments: [{lvl: 3, id: "minecraft:unbreaking"}]}')
        (1, 'minecraft', 'diamond_pickaxe', {'Enchantments': [{'lvl': 3, 'id': 'minecraft:unbreaking'}]})

        >>> parse_item('create:wrench{Unbreakable: 1b} 3')
        (3, 'create', 'wrench', {'Unbreakable': '1b'})

        >>> parse_item('minecraft:apple 64')
        (64, 'minecraft', 'apple', {})

        >>> parse_item('invalid_string')
        None
    """

    # 清理输入
    item_string = item_string.strip()
    if not item_string:
        return None

    # 模式1: 带有NBT标签的物品 (物品名{NBT} 数量)
    pattern_with_nbt = r'^([a-z0-9_.-]+):([a-z0-9_./-]+)\s*\{(.*)\}(?:\s+(\d+))?$'
    match_with_nbt = re.match(pattern_with_nbt, item_string, re.IGNORECASE)

    if match_with_nbt:
        namespace, item_id, nbt_content, count = match_with_nbt.groups()
        count = int(count) if count else 1
        nbt_dict = parse_nbt_content(nbt_content)
        return count, namespace, item_id, nbt_dict

    # 模式2: 带有NBT标签但没有数量的物品 (物品名{NBT})
    pattern_nbt_no_count = r'^([a-z0-9_.-]+):([a-z0-9_./-]+)\s*\{(.*)\}$'
    match_nbt_no_count = re.match(pattern_nbt_no_count, item_string, re.IGNORECASE)

    if match_nbt_no_count:
        namespace, item_id, nbt_content = match_nbt_no_count.groups()
        count = 1
        nbt_dict = parse_nbt_content(nbt_content)
        return count, namespace, item_id, nbt_dict

    # 模式3: 没有NBT标签但有数量的物品 (物品名 数量)
    pattern_with_count = r'^([a-z0-9_.-]+):([a-z0-9_./-]+)(?:\s+(\d+))$'
    match_with_count = re.match(pattern_with_count, item_string, re.IGNORECASE)

    if match_with_count:
        namespace, item_id, count = match_with_count.groups()
        count = int(count) if count else 1
        return count, namespace, item_id, {}

    # 模式4: 只有物品名的格式 (物品名)
    pattern_simple = r'^([a-z0-9_.-]+):([a-z0-9_./-]+)$'
    match_simple = re.match(pattern_simple, item_string, re.IGNORECASE)

    if match_simple:
        namespace, item_id = match_simple.groups()
        count = 1
        return count, namespace, item_id, {}

    return None


@logger.catch
def main() -> None:
    if not is_in_mcdr_dir():
        raise RuntimeError("当前目录不是 MCDR 服务器的根目录，请把脚本放在 MCDR 的根目录运行")

    print("请输入 MCDRpost 2.x 订单数据文件的路径")
    print("如果你没有调过配置的话，留空就好")
    data_file_path = input("path: ")

    if not data_file_path:
        data_file_path = './config/MCDRpost/PostOrders.json'

    old_data = OldOrdersData(data_file_path)
    logger.info("正在加载旧版数据文件")
    try:
        old_data.load_json()
    except FileNotFoundError:
        logger.error("未找到旧版数据文件，请检查文件路径是否正确")
        raise

    logger.info("正在转换数据结构 ...")

    new_order_data: dict[str, Order] = {}
    for order_id, old_order in old_data.orders.items():
        parse_res = parse_item(old_order['item'])

        if parse_res is None:
            logger.warning(f"非法的物品：{old_order['item']}")
            logger.warning("使用 minecraft:air 代替")
            item: Item = AIR
        else:
            count, namespace, item_id, nbt_dict = parse_res
            item: Item = Item(
                id=f'{namespace}:{item_id}',
                count=count,
                components=nbt_dict
            )

        new_order_data[order_id] = Order(
            id=int(order_id),
            time=old_order['time'],
            sender=old_order['sender'],
            receiver=old_order['receiver'],
            comment=old_order['info'],
            item=item
        )

    new_data = NewOrderData(
        players=old_data.players,
        orders=new_order_data
    ).serialize()

    logger.info("正在保存数据到 config/MCDRpost/orders.json ...")

    with open('config/MCDRpost/orders.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    with logger:
        main()
