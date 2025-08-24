#Requires -Version 5.0

param(
    [Parameter(Mandatory = $true)]
    [string]${PluginName}
)

# MCDRpost 打包脚本
# 使用 mcdreforged pack 命令将插件打包到 build 目录

Write-Host "开始打包插件: $PluginName"

# 检查插件源目录是否存在
${pluginSourcePath} = "src\$PluginName"
if (-not (Test-Path ${pluginSourcePath})) {
    Write-Error "插件源目录不存在: ${pluginSourcePath}"
    exit 1
}

# 使用 mcdreforged pack 命令打包插件
mcdreforged pack --input $pluginSourcePath --output "dist/" --ignore-file "../../.gitignore"

Write-Host "插件 ${PluginName} 打包完成！"