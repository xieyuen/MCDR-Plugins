#Requires -Version 5.0

param(
    [Parameter(Mandatory = $true)]
    [string]${PluginName}
)

# 创建插件脚本
# 在 src 目录下创建新的 MCDR 插件结构

Write-Host "开始创建插件: $PluginName"

# 定义插件路径
${pluginPath} = "src\$PluginName"

# 检查插件目录是否已存在
if (Test-Path ${pluginPath})
{
    Write-Error "插件目录已存在: ${pluginPath}"
    exit 1
}

# 创建插件目录结构
New-Item -ItemType Directory -Path ${pluginPath} | Out-Null

# 创建插件的Python包目录
${packageName} = ${PluginName}.ToLower()
New-Item -ItemType Directory -Path "${pluginPath}\${packageName}" | Out-Null

# 创建基本的插件元数据文件
${metadataContent} = @"
{
  "id": "$(${PluginName}.ToLower() )",
  "version": "0.1.0",
  "name": "$PluginName",
  "description": {
    "en_us": "A new MCDR plugin",
    "zh_cn": "一个新的MCDR插件"
  },
  "author": [
    "xieyuen"
  ],
  "dependencies": {
    "python": ">=3.10",
    "mcdreforged": ">=2.10"
  }
}
"@

${metadataContent} | Out-File -FilePath "${pluginPath}\mcdreforged.plugin.json" -Encoding UTF8

# 创建空的初始化文件
"" | Out-File -FilePath "${pluginPath}\${packageName}\__init__.py" -Encoding UTF8
"# ${PluginName}" | Out-File -FilePath "${pluginPath}\README.md" -Encoding UTF8

Write-Host "插件 ${PluginName} 创建完成！"
Write-Host "插件路径: ${pluginPath}"