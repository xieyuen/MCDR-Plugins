# KillServer

在关服卡死时强制关闭服务器

> [!WARNING]
> 此插件使用 [dowhen](http://github.com/gaogaotiantian/dowhen/) 模块实现, 可能不够稳定

## 介绍

对于下面的两种情况(实际可能还有更多适用的情况):

- Fabric 服务器卡死不关闭
  - [MCDReforged/MCDReforged#150](https://github.com/MCDReforged/MCDReforged/issues/150)
  - [EngineHub/WorldEdit#2459](https://github.com/EngineHub/WorldEdit/issues/2459)
- `pause` 命令诱发用户Ctrl+C操作，导致 MCDR 关闭与存档恢复冲突，最终致使存档损坏
  - [TISUnion/PrimeBackup#85](https://github.com/TISUnion/PrimeBackup/issues/85)


本插件提供监听服务器关闭并且在这些情况下强制关闭服务器的功能, 给小白腐竹们提供一个简单且无脑的解决方案

## 配置

本插件只有一项配置: `waiting_time`

这个配置是等待服务器关闭的时间, **单位为秒**, 默认为 60 秒

## 使用方法

直接安装到 MCDR 的插件文件夹下即可

```mcdr
!!MCDR plg install kill_server
```

安装后只需要注意服务器关闭不要用 Minecraft 原生的 `/stop` 命令, 换用 MCDR 命令来关闭,
比如 `!!MCDR server stop` `!!MCDR server restart`

> 你都用 MCDR 了竟然还不知道原生 `/stop` 会让 MCDR 关闭吗?<br>
> 你都用 MCDR 了竟然还用不支持运行时回档的备份模组而不是 PrimeBackup、QuickBackupM 吗?
