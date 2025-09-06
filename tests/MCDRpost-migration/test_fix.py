import json
import re

def fix_nbt_format(nbt_content: str) -> str:
    """修复NBT格式使其符合JSON规范。"""
    if not nbt_content:
        return "{}"

    # 先处理原始字符串，修复一些常见的格式问题
    fixed = nbt_content
    
    # 修复数字和单位之间有空格的情况，如 "lvl: 3 s" -> "lvl: \"3s\""
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*([,}])', r':"\1\2"\3', fixed)
    # 修复键值对之间的空格问题，如 "lvl: 3 s,id:" -> "lvl: \"3s\",id:"
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*,', r':"\1\2",', fixed)
    # 处理数组中的对象，修复其中的格式问题
    fixed = re.sub(r'\[\s*{', '[{', fixed)
    fixed = re.sub(r'}\s*\]', '}]', fixed)
    # 修复未加引号的键
    fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', fixed)
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
    """解析NBT内容为字典。"""
    if not nbt_content:
        return {}

    try:
        return json.loads(f"{{{nbt_content}}}")
    except json.JSONDecodeError:
        try:
            fixed_nbt = fix_nbt_format(nbt_content)
            print(f"修复后的NBT: {fixed_nbt}")
            return json.loads(fixed_nbt)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return {"raw_nbt": nbt_content}

# 测试有问题的完整物品字符串
test_item = 'minecraft:diamond_pickaxe{Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]}'
print(f"测试物品字符串: {test_item}")

# 提取NBT部分进行测试
nbt_start = test_item.find('{')
nbt_end = test_item.rfind('}')
if nbt_start != -1 and nbt_end != -1:
    nbt_content = test_item[nbt_start+1:nbt_end]
    print(f"提取的NBT内容: {nbt_content}")
    
    # 尝试解析NBT
    result = parse_nbt_content(nbt_content)
    print(f"解析结果: {result}")
else:
    print("无法提取NBT内容")