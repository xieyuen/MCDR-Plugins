# MCDRpost Migration

## Introduce

这是 MCDRpost 2.x -> 3.x 的升级工具

由于 Minecraft 1.20.5 使用新的 components 系统替换了原来的 tag 标签，
导致 MCDRpost 2.x 无法执行 `item replace` 命令，
因此，xieyuen 在 3.3.0 版本的更新中重构了

## Usage

把 `migration.py` 放到 MCDR 的根目录，双击打开或者使用 `python migration.py` 均可

接着在命令行中跟着提示输入订单数据文件的路径（通常是在 `config/MCDRpost/` 中，如果你没有改过配置的话），然后等待完成即可

> [!NOTE]
> 如果你没有改过配置，那么在填入订单数据文件的路径时可以留空
