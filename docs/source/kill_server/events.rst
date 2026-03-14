KillServer API -- Events
============================

.. py:currentmodule:: kill_server

KillServer 创建了一些新的事件用以监听服务器的运行状态.
对于 MCDR 内置的一些生命周期事件本插件继续沿用, 并补充了不少
生命周期中的其他事件, 它们都是 :class:`ServerEvent` 的实例

.. autoclass:: ServerEvent

下面是 KillServer 创建的所有事件和 MCDR 服务端控制事件的集合类,
在使用时, 推荐使用此类或直接使用事件 ID

.. autoclass:: ServerEvents
