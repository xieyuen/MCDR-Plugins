import sys
import os

# 将src目录添加到路径中，以便可以导入migration模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'MCDRpost-migration'))

from migration import parse_item, parse_nbt_content
import json


def test_problematic_nbt():
    """测试有问题的NBT内容"""
    # 测试NBT内容
    nbt_content = 'Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]'
    print("=== 测试NBT内容解析 ===")
    print(f"原始NBT内容: {nbt_content}")
    
    result = parse_nbt_content(nbt_content)
    print(f"解析结果: {result}")
    
    # 验证结果
    if isinstance(result, dict) and "Enchantments" in result:
        enchantments = result["Enchantments"]
        if isinstance(enchantments, list) and len(enchantments) > 0:
            enchantment = enchantments[0]
            if isinstance(enchantment, dict) and "lvl" in enchantment and "id" in enchantment:
                print("NBT解析测试通过")
                return True
    
    print("NBT解析测试失败")
    return False


def test_full_item():
    """测试完整物品字符串解析"""
    test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
    print("\n=== 测试完整物品解析 ===")
    print(f"测试物品: {test_item}")
    
    result = parse_item(test_item)
    print(f"解析结果: {result}")
    
    if result is not None:
        count, namespace, item_id, nbt_dict = result
        print(f"解析成功 - 数量: {count}, 命名空间: {namespace}, 物品ID: {item_id}, NBT: {nbt_dict}")
        
        # 验证NBT内容是否正确解析
        if "Enchantments" in nbt_dict:
            enchantments = nbt_dict["Enchantments"]
            if isinstance(enchantments, list) and len(enchantments) > 0:
                enchantment = enchantments[0]
                if isinstance(enchantment, dict) and "lvl" in enchantment and "id" in enchantment:
                    print("完整物品解析测试通过")
                    return True
    
    print("完整物品解析测试失败")
    return False


if __name__ == "__main__":
    nbt_success = test_problematic_nbt()
    item_success = test_full_item()
    
    if not (nbt_success and item_success):
        sys.exit(1)
    else:
        print("\n所有测试通过!")