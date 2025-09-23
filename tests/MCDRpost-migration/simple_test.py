import sys
sys.path.append('../../src/MCDRpost-migration')
from migration import parse_item

# 测试有问题的物品字符串
test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'

print(f"测试物品字符串: {test_item}")
result = parse_item(test_item)

if result:
    print(f"解析成功: {result}")
else:
    print("解析失败")