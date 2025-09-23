import sys
import os

# 将src目录添加到路径中，以便可以导入migration模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'MCDRpost-migration'))

from migration import parse_item


def test_problematic_item():
    """测试有问题的完整物品字符串"""
    test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
    print(f"测试物品字符串: {test_item}")

    # 尝试解析整个物品
    result = parse_item(test_item)
    print(f"解析结果: {result}")
    
    # 验证结果是否符合预期
    if result is not None:
        count, namespace, item_id, nbt_dict = result
        print(f"数量: {count}")
        print(f"命名空间: {namespace}")
        print(f"物品ID: {item_id}")
        print(f"NBT字典: {nbt_dict}")
        
        # 检查是否包含预期的键
        if "Enchantments" in nbt_dict:
            enchantments = nbt_dict["Enchantments"]
            if isinstance(enchantments, list) and len(enchantments) > 0:
                enchantment = enchantments[0]
                if "lvl" in enchantment and "id" in enchantment:
                    print("测试通过：物品已成功解析")
                    return True
    
    print("测试失败：物品未正确解析")
    return False


if __name__ == "__main__":
    success = test_problematic_item()
    if success:
        print("\n修复成功！")
    else:
        print("\n修复失败！")
        sys.exit(1)