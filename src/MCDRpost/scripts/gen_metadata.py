import json
import tomllib


def gen_metadata():
    metadata = {
        "id": "mcdrpost",
        "name": "MCDRpost",
        "description": {
            "en_us": "A MCDR plugin for post/teleport items",
            "zh_cn": "一个用于邮寄/传送物品的MCDR插件"
        },
        "author": [
            "Flyky",
            "xieyuen"
        ],
        "link": "https://github.com/xieyuen/MCDRpost/",
        "dependencies": {
            "python": ">=3.10",
            "mcdreforged": ">=2.0.1",
            "minecraft_data_api": "*"
        },
        "resources": [
            "lang"
        ]
    }

    with open("pyproject.toml", "rb") as f:
        version = tomllib.load(f)['project']['version']

    metadata['version'] = version

    with open("mcdreforged.plugin.json", "w") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
