# Develop Handler

这是一个为方便测试 MCDR 插件交互的 Handler，让 MCDR 能够识别 `say` 的输出

## Background

我在开发 [MCDRpost](../MCDRpost/README.md) 的时候会想着测试交互有没有问题，但是又不想开 Minecraft 客户端，
也暂时不想看客户端的信息，就想使用 `execute as Test run say <command>` 直接代替假人发送命令来测试，
但是直接 `say` MCDR 是不识别的

因为输出是这样的：

```log
[11:02:30] [Server thread/INFO]: [Not Secure] [Test] !!po pl
```

而 Minecraft 原版服务端一般的玩家聊天输出是这样的：

```log
[11:02:30] [Server thread/INFO]: <Test> !!po pl
```

这就导致 MCDR 不会响应命令，所以我写了它

## Features

让 MCDR 能够识别 `say` 的输出

## Dependencies

Minecraft 服务端应该是 Carpet 服务端~~不然假人哪来的~~

## Weaknesses

> [!WARNING]
> MCDR 终端上的输出格式**会被改变**，这将导致终端输出和日志内容不统一
>
> `say` 的部分在 latest.log 中仍然保持 `[Not Secure] [Player]` 的形式，但是终端的显示将会是 `<Player>` <br>
> 如果你不能接受的话，请不要使用本插件
