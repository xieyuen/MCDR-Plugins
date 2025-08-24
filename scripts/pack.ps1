#Requires -Version 5.0

param(
    [Parameter(Mandatory = $true)]
    [string]${PluginName}
)

# MCDRpost ����ű�
# ʹ�� mcdreforged pack ����������� build Ŀ¼

Write-Host "��ʼ������: $PluginName"

# �����ԴĿ¼�Ƿ����
${pluginSourcePath} = "src\$PluginName"
if (-not (Test-Path ${pluginSourcePath})) {
    Write-Error "���ԴĿ¼������: ${pluginSourcePath}"
    exit 1
}

# ʹ�� mcdreforged pack ���������
mcdreforged pack --input $pluginSourcePath --output "dist/" --ignore-file "../../.gitignore"

Write-Host "��� ${PluginName} �����ɣ�"