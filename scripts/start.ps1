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
    [Alias("n", "ns", "no-start")]
    [switch]$nostart
)


Set-Location ./test/

try
{
    if ($nostart)
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
}
finally
{
    # �ָ�ԭʼĿ¼
    Set-Location ..
}