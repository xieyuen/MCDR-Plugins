import importlib
from pathlib import Path


def register_all_handlers():
    """自动导入version_handler目录下所有模块（除了__init__.py和abstract_version_handler.py）

    通过动态导入所有版本处理器模块，触发它们的自动注册机制
    """
    # 获取当前模块所在目录
    builtin_handlers = Path(__file__).parent / 'builtins'

    # 遍历目录中的所有.py文件
    for file_path in builtin_handlers.glob("*.py"):
        # 动态导入模块，触发其中的注册代码
        importlib.import_module(f"mcdrpost.version_handler.{file_path.stem}")
