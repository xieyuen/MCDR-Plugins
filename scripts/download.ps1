param(
    [Parameter(Mandatory = $true)]
    [string]${PluginId}
)

Write-Host "��ʼ���ز��: ${PluginId}"

mcdreforged pim download --output "dependencies/" ${PluginId}

Write-Host "��� ${PluginId} �������"
