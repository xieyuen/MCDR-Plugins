#Requires -Version 5.0

<#
.SYNOPSIS
����MCDR�������ű�

.DESCRIPTION
��������λ��testĿ¼�µ�MCDR��������֧��--no-startѡ��������ʼ��������������������

.PARAMETER NoStart
��ѡ���������ָ����ֻ��ʼ��������������������

.EXAMPLE
./scripts/start.ps1
����MCDR������

.EXAMPLE
./scripts/start.ps1 -NoStart
��ʼ��������������������

#>

param(
    [Alias("n")]
    [switch]$NoStart
)


cd ./test/

if ($NoStart)
{
    Write-Host "������ --no-server-start �������� MCDR"
    mcdreforged start --no-server-start
}
else
{
    # ����MCDR������
    Write-Host "�������� MCDR ������..."
    mcdreforged start
}

# �ָ�ԭʼĿ¼
cd ..
