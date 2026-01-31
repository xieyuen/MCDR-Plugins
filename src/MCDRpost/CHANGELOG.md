# 更新日志

所有重要的变更都会记录在这个文件中。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- 新增配置检查

## [3.4.0-beta.1]

### Changed

- update mcdr version requirements to 2.16.5 for adaptation to new Minecraft version system
- 正式启用 MinecraftVersion 类
- 格式化了部分代码
- 命令等字面量提取重构

## [3.4.0-alpha.4]

### Added

- 在 dependencies 引入 submodule (MinecraftDataAPI)

### Changed

- 迁移脚本和部分模块有些许变化，但无大影响

> [!NOTE]
> 迁移脚本没有发布在 release 中

### Removed

- 删除了无用的 Exception
- 放弃单独的 3.12 支持开发分支
- 放弃 AI 修改版本 (Tag: mcdrpost-v3.4.0-rc.1+build.ai.lingma) 的支持

## [3.4.0-alpha.3]

### Added

- 新开分支专门准备放弃 Python 3.10 的版本

### Changed

- 内置处理器的条件函数替换成元组比较

## [3.4.0-alpha.2]

### Added

- 补充了一些类型注解
- 添加弃用提示

### Changed

- 简化协调器模块的命名

### Deprecated

|       弃用的配置        |          新配置           |
|:------------------:|:----------------------:|
|  command_prefixed  |   prefix.more_prefix   |
|    allow_alias     | prefix.enable_addition |
| command_permission |      permissions       |

## [3.4.0-alpha.1]

### Added

- `env.server_version` 支持元组比较
    - e.g. `env.server_version >= (1, 20, 5)`
- 补充了 TranslationKeyItem 的 docstring

### Changed

- 重构了 CommandManager, 分离 UI 和命令解析
    - 新增 CommandPreHandler 处理解析的类型与功能类的交互
- 重构了 PostManager, 保持邮寄核心功能的单一职责
    - 添加了 MCDRpostCoordinator 类作为协调器

## [3.3.3]

### Fixed

- 修复了无法发送/接受物品的 BUG

## [3.3.3-beta.2]

### Added

- 提供自定义音效的 API
    - 删除了原本的 play_sound 模块
    - 添加抽象类: AbstractSoundPlayer
    - 添加实现类: NewSoundPlayer 并暴露至 API
    - 添加实现类: OldSoundPlayer 并暴露至 API
    - 添加 property: AbstractVersionHandler.play_sound
- 添加了一些注释和类型注解

### Changed

- 修改了部分变量/属性的名称

|              原名称              |                  新名称                   |
|:-----------------------------:|:--------------------------------------:|
| TranslationKeyItem.__FULL_KEY | TranslationKeyItem.__FULL_KEY_TEMPLATE |
|         utils.__Node          |            utils.__NodeType            |

## [3.3.3-beta.1]

### Changed

- 新的翻译使用方式
    - 原来的 `tr(Tags.xxx)` 使用方法还是不够方便，换成 `TranslationKeys.xxx.tr()` 就不用再在外面套一层 `tr()` 了

## [3.3.3-alpha.3]

### Fixed

- 修复了 player 命令没有回复的问题

## [3.3.3-alpha.2]

### Changed

- 放弃对 1.9~1.13 的支持，当服务器使用此区间的版本时只使用外界注册的 Handler

## [3.3.2] - [YANKED]

> [!CAUTION]
> Due to a critical bug, this version is yanked.

## [3.3.2-rc.2] - 2025-09-21

### Added

- 新增错误提示，保证用户体验

### Removed

- 删除了无意义的 `__all__` 变量

## [3.3.2-rc.1] - 2025-09-21

### Fixed

修复了玩家无法接受物品的问题

## [3.3.2-beta5] - 2025-09-20

### Changed

- 重构了 `AbstractVersionHandler` 类
    - 删除了 `item2str` 和 `dict2item` 方法
    - 新增了 (abstractmethod) `get_offhand_item` 方法
    - `is_builtin` 不再是 property 而是 classmethod
- 重构了 `BulitinVersionHandler`
    - 新增 `get_offhand_item` 实现
    - 新增 `replace` 实现（仅在 `Since9Handler` 中被覆盖）
    - 新增 (abstractmethod) `item2str` 方法
    - 新增 (abstractmethod) `dict2item` 方法

### Added

- 新增了 `DefaultVersionHandler` 类并且暴露至 api
- API
    - 暴露 `DefaultVersionHandler` 类
    - 暴露 `OFFHAND_CODE` 常量

## [3.3.2-beta4]

### Added

- 实现了自定义 Handler

## [3.3.2-beta3]

### Removed

- 删除了 `utils.types` 模块
- 删除了一些没有用的方法/函数
- 删除了 `reload` `save` 命令及其权限配置信息

### Changed

- 重命名 `before17` 为 `since9`
- 新增 `reload` 子命令，用于重新加载配置文件和订单数据

### Fixed

- 修复反序列化失败的问题
- 修复在插件加载阶段时如果订单无效翻译出错的问题
- 修复了插件加载时的翻译报错问题

## [3.3.2-beta2]

### Changed

- 重构 `version_handler` 模块

## [3.3.2-beta1]

### Removed

- 删除了 `reload` `save` 命令及其权限配置信息

### Fixed

- 修复了插件加载时的翻译报错问题

## [3.3.1]

### Changed

- 获得了 Flyky 的授权，更新 MCDRpost 在插件仓库的信息

## [3.3.0]

> [!WARNING]
> 此版本和旧版本不兼容，需要更新数据文件

### Added

实现对 Minecraft 1.20.5 版本及以上的支持

- 改变了原来订单中物品的储存方式，拆分得更加细致

## [3.2.1]

### Changed

- 使用 MCDR 2.15.0 的新特性，MCDRpost 不再支持低于 2.15.0 以下的版本

## [3.2.0]

### Added

- 添加了新玩家登录时是否自动注册的配置

## [3.1.2]

### Added

- 添加了命令的权限配置

## [3.0.0]

### Changed

重构了旧代码，具体包括：

- 模块化重构
- 利用面向对象实现 MCDRpost 主要功能
- 增加了配置文件
- 修改了原来的订单管理系统，并且使用 `server.load_config_simple` 和 `server.save_config_simple` 实现订单数据的加载和保存
- 拆分了冗长的 `__init__.py`，用几个 Manager 代替

## [2.1.1]

### Fixed

- 修复了插件不能加载的问题 (Flyky/MCDRpost#8)
