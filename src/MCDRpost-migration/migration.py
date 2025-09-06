import json
import os.path
import re
from typing import Any

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


def fix_nbt_format(nbt_content_: str) -> str:
    """修复NBT格式使其符合JSON规范。"""
    if not nbt_content_:
        return "{}"

    # 修复未加引号的键
    fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', nbt_content_)
    # 修复布尔值
    fixed = re.sub(r':\s*(true|false)\s*([,}])', r':"\1"\2', fixed)
    # 修复数字后缀
    fixed = re.sub(r':\s*(\d+)([bslfd])\s*([,}])', r':"\1\2"\3', fixed)
    # 确保字符串有引号
    fixed = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,}])', r':"\1"\2', fixed)
    # 修复数组中的字符串
    fixed = re.sub(r'\[\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\]', r'["\1"]', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*,', r',"\1",', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\]', r',"\1"]', fixed)

    return f"{{{fixed}}}"


def parse_nbt_content(nbt_content_: str) -> dict[str, Any]:
    """解析NBT内容为字典。"""
    if not nbt_content_:
        return {}

    try:
        return json.loads(f"{{{nbt_content_}}}")
    except json.JSONDecodeError:
        try:
            fixed_nbt = fix_nbt_format(nbt_content_)
            return json.loads(fixed_nbt)
        except json.JSONDecodeError:
            return {"raw_nbt": nbt_content_}


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

    Raises:
        不会显式抛出异常，但解析失败时返回None。

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

    # 模式1: 带有NBT标签的物品
    pattern_with_nbt = r'^([a-z0-9_]+):([a-z0-9_/]+)\s*\{([^}]*)\}(?:\s+(\d+))?$'
    match_with_nbt = re.match(pattern_with_nbt, item_string, re.IGNORECASE)

    if match_with_nbt:
        namespace, item_id, nbt_content, count = match_with_nbt.groups()
        count = int(count) if count else 1
        nbt_dict = parse_nbt_content(nbt_content)
        return count, namespace, item_id, nbt_dict

    # 模式2: 纯物品（无NBT标签）
    pattern_simple = r'^([a-z0-9_]+):([a-z0-9_/]+)(?:\s+(\d+))?$'
    match_simple = re.match(pattern_simple, item_string, re.IGNORECASE)

    if match_simple:
        namespace, item_id, count = match_simple.groups()
        count = int(count) if count else 1
        return count, namespace, item_id, {}

    return None


def main() -> None:
    if not is_in_mcdr_dir():
        raise RuntimeError("当前目录不是 MCDR 服务器的根目录，请把脚本放在 MCDR 的根目录运行")

    print("请输入 MCDRpost 2.x 订单数据文件的路径")
    print("如果你没有调过配置的话，留空就好")
    data_file_path = input("path: ")

    if not data_file_path:
        data_file_path = 'PostOrders.json'

    old_data = OldOrdersData(data_file_path)
    print("正在加载旧版数据文件")
    try:
        old_data.load_json()
    except FileNotFoundError:
        print("Error: 未找到旧版数据文件，请检查文件路径是否正确")
        raise

    print("正在转换数据结构 ...")

    new_order_data: dict[str, Order] = {}
    for order_id, old_order in old_data.orders.items():
        count, namespace, item_id, nbt_dict = parse_item(old_order['item'])
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
            comment=old_order['comment'],
            item=item
        )

    new_data = dict(
        players=old_data.players,
        orders=new_order_data
    )

    print("正在保存数据到 config/MCDRpost/orders.json ...")

    with open('config/MCDRpost/orders.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
