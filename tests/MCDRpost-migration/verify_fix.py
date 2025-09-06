import sys
import os

# 将src目录添加到路径中，以便可以导入migration模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'MCDRpost-migration'))

from migration import parse_item


def test_parse_item():
    """测试物品解析函数"""
    test_cases = [
        'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}',
        'create:wrench{Unbreakable: 1b} 3',
        'minecraft:apple 64',
        'botania:mana_tablet'
    ]
    
    for i, test_item in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_item}")
        result = parse_item(test_item)
        print(f"解析结果: {result}")
        
        if result is not None:
            count, namespace, item_id, nbt_dict = result
            print(f"  数量: {count}")
            print(f"  命名空间: {namespace}")
            print(f"  物品ID: {item_id}")
            print(f"  NBT字典: {nbt_dict}")
            print("  ✓ 解析成功")
        else:
            print("  ✗ 解析失败")


if __name__ == "__main__":
    test_parse_item()