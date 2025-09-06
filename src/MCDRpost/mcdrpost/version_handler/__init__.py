import importlib
from pathlib import Path


def register_all_handlers():
    """自动导入 version_handler/impl 目录下所有模块

    通过动态导入所有版本处理器模块，触发它们的自动注册机制
    """
    # 获取当前模块所在目录
    builtin_handlers = Path(__file__).parent / 'impl'

    # 遍历目录中的所有.py文件
    for file_path in builtin_handlers.glob("*.py"):
        # 动态导入模块，触发其中的注册代码
        importlib.import_module(f"mcdrpost.version_handler.impl.{file_path.stem}")
