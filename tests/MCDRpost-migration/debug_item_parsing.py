import sys
import os

# 将src目录添加到路径中，以便可以导入migration模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'MCDRpost-migration'))

from migration import parse_item
import re


def debug_parse_item(item_string: str):
    """调试版本的物品解析函数"""
    print(f"=== 调试物品解析 ===")
    print(f"输入物品字符串: {item_string}")

    # 清理输入
    item_string = item_string.strip()
    if not item_string:
        print("空字符串，返回None")
        return None

    print("尝试匹配各种模式...")

    # 模式1: 带有NBT标签的物品 (物品名{NBT} 数量)
    pattern_with_nbt = r'^([a-z0-9_.-]+):([a-z0-9_.-/]+)\s*\{([^}]*)\}(?:\s+(\d+))?$'
    match_with_nbt = re.match(pattern_with_nbt, item_string, re.IGNORECASE)
    print(f"模式1匹配结果: {match_with_nbt}")

    if match_with_nbt:
        namespace, item_id, nbt_content, count = match_with_nbt.groups()
        print(f"  匹配成功:")
        print(f"    命名空间: {namespace}")
        print(f"    物品ID: {item_id}")
        print(f"    NBT内容: {nbt_content}")
        print(f"    数量: {count}")
        return "pattern1", (namespace, item_id, nbt_content, count)

    # 模式2: 带有NBT标签但没有数量的物品 (物品名{NBT})
    pattern_nbt_no_count = r'^([a-z0-9_.-]+):([a-z0-9_.-/]+)\s*\{([^}]*)\}$'
    match_nbt_no_count = re.match(pattern_nbt_no_count, item_string, re.IGNORECASE)
    print(f"模式2匹配结果: {match_nbt_no_count}")

    if match_nbt_no_count:
        namespace, item_id, nbt_content = match_nbt_no_count.groups()
        print(f"  匹配成功:")
        print(f"    命名空间: {namespace}")
        print(f"    物品ID: {item_id}")
        print(f"    NBT内容: {nbt_content}")
        return "pattern2", (namespace, item_id, nbt_content)

    # 模式3: 没有NBT标签但有数量的物品 (物品名 数量)
    pattern_with_count = r'^([a-z0-9_.-]+):([a-z0-9_.-/]+)(?:\s+(\d+))$'
    match_with_count = re.match(pattern_with_count, item_string, re.IGNORECASE)
    print(f"模式3匹配结果: {match_with_count}")

    if match_with_count:
        namespace, item_id, count = match_with_count.groups()
        print(f"  匹配成功:")
        print(f"    命名空间: {namespace}")
        print(f"    物品ID: {item_id}")
        print(f"    数量: {count}")
        return "pattern3", (namespace, item_id, count)

    # 模式4: 只有物品名的格式 (物品名)
    pattern_simple = r'^([a-z0-9_.-]+):([a-z0-9_.-/]+)$'
    match_simple = re.match(pattern_simple, item_string, re.IGNORECASE)
    print(f"模式4匹配结果: {match_simple}")

    if match_simple:
        namespace, item_id = match_simple.groups()
        print(f"  匹配成功:")
        print(f"    命名空间: {namespace}")
        print(f"    物品ID: {item_id}")
        return "pattern4", (namespace, item_id)

    print("所有模式都无法匹配，返回None")
    return None


def test_debug():
    """测试调试函数"""
    test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
    result = debug_parse_item(test_item)
    print(f"\n最终结果: {result}")
    return result


if __name__ == "__main__":
    test_debug()