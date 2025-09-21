# 更新日志

所有重要的变更都会记录在这个文件中。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)。

## [Unreleased]

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
