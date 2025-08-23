param(
    [Parameter(Mandatory = $true)]
    [string]${PluginId}
)

Write-Host "开始下载插件: ${PluginId}"

mcdreforged pim download --output "dependencies/" ${PluginId}

Write-Host "插件 ${PluginId} 下载完成"
