import json
import re
import sys
import os

# 将src目录添加到路径中，以便可以导入migration模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'MCDRpost-migration'))

from migration import fix_nbt_format, parse_nbt_content


def test_problematic_item():
    """测试有问题的完整物品字符串"""
    test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
    print(f"测试物品字符串: {test_item}")

    # 提取NBT部分进行测试
    nbt_start = test_item.find('{')
    nbt_end = test_item.rfind('}')
    if nbt_start != -1 and nbt_end != -1:
        nbt_content = test_item[nbt_start + 1:nbt_end]
        print(f"提取的NBT内容: {nbt_content}")

        # 尝试解析NBT
        result = parse_nbt_content(nbt_content)
        print(f"解析结果: {result}")
        
        # 验证结果是否符合预期
        expected_keys = ["Enchantments"]
        if isinstance(result, dict) and all(key in result for key in expected_keys):
            print("测试通过：NBT内容已成功解析")
            return True
        else:
            print("测试失败：NBT内容未正确解析")
            return False
    else:
        print("无法提取NBT内容")
        return False


if __name__ == "__main__":
    success = test_problematic_item()
    if not success:
        sys.exit(1)
