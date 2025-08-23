#Requires -Version 5.0

<#
.SYNOPSIS
启动MCDR服务器脚本

.DESCRIPTION
用于启动位于test目录下的MCDR服务器，支持--no-start选项来仅初始化环境但不启动服务器

.PARAMETER NoStart
可选参数，如果指定则只初始化环境但不启动服务器

.EXAMPLE
./scripts/start.ps1
启动MCDR服务器

.EXAMPLE
./scripts/start.ps1 -NoStart
初始化环境但不启动服务器

#>

param(
    [Alias("n")]
    [switch]$NoStart
)


cd ./test/

if ($NoStart)
{
    Write-Host "正在以 --no-server-start 参数启动 MCDR"
    mcdreforged start --no-server-start
}
else
{
    # 启动MCDR服务器
    Write-Host "正在启动 MCDR 服务器..."
    mcdreforged start
}

# 恢复原始目录
cd ..
