KillServer
==========

在关服卡死时强制关闭服务器

.. warning::
   此插件使用 `dowhen <http://github.com/gaogaotiantian/dowhen/>`_ 模块实现, 可能不够稳定

.. tip::
   BUG Report: `GitHub issues <https://github.com/xieyuen/MCDR-Plugins/issues/new>`_

介绍
----

对于下面的情况(实际可能还有更多适用的情况):

1. Fabric 服务器卡死不关闭
    - `MCDReforged/MCDReforged#150 <https://github.com/MCDReforged/MCDReforged/issues/150>`_
    - `EngineHub/WorldEdit#2459 <https://github.com/EngineHub/WorldEdit/issues/2459>`_
2. ``pause`` 命令诱发用户Ctrl+C操作，导致 MCDR 关闭与存档恢复冲突，最终致使存档损坏
    - `TISUnion/PrimeBackup#85 <https://github.com/TISUnion/PrimeBackup/issues/85>`_
    - `MCDReforged/MCDReforged#394 <https://github.com/MCDReforged/MCDReforged/issues/394>`_

本插件提供监听服务器关闭并且在这些情况下强制关闭服务器的功能, 给小白腐竹们提供一个简单且无脑的解决方案

使用方法
--------

直接安装到 MCDR 的插件文件夹下即可, 可以从 `GitHub <https://github/xieyuen/MCDR-Plugins>`_
或 `PluginCatalogue <https://mcdreforged.com/zh-CN/plugin/kill_server>`_ 手动下载插件文件

你也可以用下面的 MCDR 命令安装 KillServer

.. code-block::

   !!MCDR plg install kill_server

安装后只需要注意服务器关闭不要用 Minecraft 原生的 ``/stop`` 命令, 换用 MCDR 命令来关闭,
比如 ``!!MCDR server stop`` ``!!MCDR server restart``

> 你都用 MCDR 了竟然还不知道原生 ``/stop`` 会让 MCDR 关闭吗?<br>
> 你都用 MCDR 了竟然还用不支持运行时回档的备份模组而不是 PrimeBackup、QuickBackupM 吗?

配置
----

.. list-table::
   :widths: 20 15 20 40 15
   :header-rows: 1

   * - 配置项
     - 类型
     - 默认值
     - 含义
     - 注释
   * - ``enable``
     - ``bool``
     - ``True``
     - 是否启用插件
     - 不影响事件分发
   * - ``waiting_time``
     - ``float``
     - ``60``
     - 等待服务器关闭的时间, 超时强制关闭
     - 单位为秒
   * - ``mcdr_only``
     - ``bool``
     - ``False``
     - 是否只监听 `PluginStoppingServerEvent`
     -

新的事件
--------

见 :doc:`events`
