import re

def detailed_debug():
    """详细调试正则表达式匹配"""
    test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
    print(f"测试字符串: {test_item}")
    
    # 检查各种可能的正则表达式
    
    # 原始模式
    pattern_original = r'^([a-z0-9_.-]+):([a-z0-9_.-/]+)\s*\{([^}]*)\}(?:\s+(\d+))?$'
    match_original = re.match(pattern_original, test_item, re.IGNORECASE)
    print(f"\n原始模式: {pattern_original}")
    print(f"匹配结果: {match_original}")
    if match_original:
        print(f"捕获组: {match_original.groups()}")
    
    # 修正后的模式
    pattern_fixed = r'^([a-z0-9_.-]+):([a-z0-9_.\-/]+)\s*\{([^}]*)\}(?:\s+(\d+))?$'
    match_fixed = re.match(pattern_fixed, test_item, re.IGNORECASE)
    print(f"\n修正后模式: {pattern_fixed}")
    print(f"匹配结果: {match_fixed}")
    if match_fixed:
        print(f"捕获组: {match_fixed.groups()}")
    
    # 更宽松的模式
    pattern_loose = r'^([a-z0-9_.-]+):([a-z0-9_.\-/]+)\s*{(.*)}(?:\s+(\d+))?$'
    match_loose = re.match(pattern_loose, test_item, re.IGNORECASE)
    print(f"\n宽松模式: {pattern_loose}")
    print(f"匹配结果: {match_loose}")
    if match_loose:
        print(f"捕获组: {match_loose.groups()}")
        
    # 最宽松的模式
    pattern_most_loose = r'^([a-z0-9_.-]+):([a-z0-9_.\-/]+)\s*{(.*)}'
    match_most_loose = re.match(pattern_most_loose, test_item, re.IGNORECASE)
    print(f"\n最宽松模式: {pattern_most_loose}")
    print(f"匹配结果: {match_most_loose}")
    if match_most_loose:
        print(f"捕获组: {match_most_loose.groups()}")
        
    # 分步测试
    print("\n=== 分步测试 ===")
    # 只匹配物品部分
    pattern_item = r'^([a-z0-9_.-]+):([a-z0-9_.\-/]+)'
    match_item = re.match(pattern_item, test_item, re.IGNORECASE)
    print(f"物品匹配模式: {pattern_item}")
    print(f"匹配结果: {match_item}")
    if match_item:
        print(f"捕获组: {match_item.groups()}")
        
    # 只匹配NBT部分
    pattern_nbt = r'\{(.*)\}'
    match_nbt = re.search(pattern_nbt, test_item, re.IGNORECASE)
    print(f"\nNBT匹配模式: {pattern_nbt}")
    print(f"匹配结果: {match_nbt}")
    if match_nbt:
        print(f"捕获组: {match_nbt.groups()}")

if __name__ == "__main__":
    detailed_debug()