<#
.SYNOPSIS
    安装 major-learning-coach 技能到 Claude Code 或 DeepSeek Harness 的技能目录。

.EXAMPLE
    .\install.ps1                      # 两个都装
    .\install.ps1 -Target dsh          # 只装到 ~/.agents/skills
    .\install.ps1 -Dest D:\skills -Force
#>
[CmdletBinding()]
param(
    [ValidateSet('dsh', 'claude', 'both')]
    [string]$Target = 'both',

    [string]$Dest = '',

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

# Windows PowerShell 5.1 控制台默认不是 UTF-8，中文会乱码
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$src = Join-Path $root 'skills/major-learning-coach'
if (-not (Test-Path -LiteralPath $src)) {
    throw "找不到技能源目录：$src（请在仓库根目录运行本脚本）"
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$destinations = @()

if ($Dest) {
    $destinations += $Dest
}
else {
    if ($Target -in @('dsh', 'both')) { $destinations += (Join-Path $HOME '.agents/skills') }
    if ($Target -in @('claude', 'both')) { $destinations += (Join-Path $HOME '.claude/skills') }
}

foreach ($base in $destinations) {
    New-Item -ItemType Directory -Path $base -Force | Out-Null
    $dst = Join-Path $base 'major-learning-coach'

    if (Test-Path -LiteralPath $dst) {
        if (-not $Force) {
            $backup = "$dst.bak.$stamp"
            Copy-Item -LiteralPath $dst -Destination $backup -Recurse -Force
            Write-Host "已备份旧版本 -> $backup"
        }
        Remove-Item -LiteralPath $dst -Recurse -Force
    }

    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
    $count = (Get-ChildItem -Path (Join-Path $dst 'majors') -Directory | Where-Object { $_.Name -notlike '_*' }).Count
    Write-Host "已安装 -> $dst（$count 个专业）"
}

Write-Host ''
Write-Host '下一步：新开一个会话，说「我是计科的，想系统学一遍」，或「这道题怎么做：...」。'
Write-Host '若技能没被触发，确认目标目录在客户端的 skills 搜索路径内，然后重启会话。'
