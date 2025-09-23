import json
import re


def fix_nbt_format(nbt_content: str) -> str:
    """修复NBT格式使其符合JSON规范。"""
    if not nbt_content:
        return "{}"

    # 先处理原始字符串，修复一些常见的格式问题
    # 修复数字和单位之间有空格的情况，如 "lvl: 3 s" -> "lvl: \"3s\""
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*([,}])', r':"\1\2"\3', nbt_content)
    # 修复键值对之间的空格问题，如 "lvl: 3 s,id:" -> "lvl: \"3s\",id:"
    fixed = re.sub(r':\s*(\d+)\s+([bslfd])\s*,', r':"\1\2",', fixed)
    # 修复未加引号的键
    fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', fixed)
    # 修复布尔值
    fixed = re.sub(r':\s*(true|false)\s*([,}])', r':"\1"\2', fixed)
    # 修复数字后缀
    fixed = re.sub(r':\s*(\d+)([bslfd])\s*([,}])', r':"\1\2"\3', fixed)
    # 确保字符串有引号
    fixed = re.sub(r':\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,}])', r':"\1"\2', fixed)
    # 修复数组中的字符串
    fixed = re.sub(r'\[\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*]', r'["\1"]', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*,', r',"\1",', fixed)
    fixed = re.sub(r',\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*]', r',"\1"]', fixed)

    return f"{{{fixed}}}"


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


if __name__ == '__main__':
    # 测试有问题的NBT字符串
    test_nbt = 'Enchantments: [{lvl: 3 s,id: "minecraft:unbreaking"}]'
    print(f"原始NBT: {test_nbt}")

    try:
        result = parse_nbt_content(test_nbt)
        print(f"解析结果: {result}")
    except Exception as e:
        print(f"解析失败: {e}")
