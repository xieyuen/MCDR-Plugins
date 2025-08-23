#Requires -Version 5.0

param(
    [Parameter(Mandatory = $true)]
    [string]${PluginName}
)

# ��������ű�
# �� src Ŀ¼�´����µ� MCDR ����ṹ

Write-Host "��ʼ�������: $PluginName"

# ������·��
${pluginPath} = "src\$PluginName"

# �����Ŀ¼�Ƿ��Ѵ���
if (Test-Path ${pluginPath})
{
    Write-Error "���Ŀ¼�Ѵ���: ${pluginPath}"
    exit 1
}

# �������Ŀ¼�ṹ
New-Item -ItemType Directory -Path ${pluginPath} | Out-Null

# ���������Python��Ŀ¼
${packageName} = ${PluginName}.ToLower()
New-Item -ItemType Directory -Path "${pluginPath}\${packageName}" | Out-Null

# ���������Ĳ��Ԫ�����ļ�
${metadataContent} = @"
{
  "id": "$(${PluginName}.ToLower() )",
  "version": "0.1.0",
  "name": "$PluginName",
  "description": {
    "en_us": "A new MCDR plugin",
    "zh_cn": "һ���µ�MCDR���"
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

# �����յĳ�ʼ���ļ�
"" | Out-File -FilePath "${pluginPath}\${packageName}\__init__.py" -Encoding UTF8
"# ${PluginName}" | Out-File -FilePath "${pluginPath}\README.md" -Encoding UTF8

Write-Host "��� ${PluginName} ������ɣ�"
Write-Host "���·��: ${pluginPath}"