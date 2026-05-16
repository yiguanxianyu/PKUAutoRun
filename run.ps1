$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
$main = Join-Path $PSScriptRoot "main.py"

if (-not (Test-Path $py)) {
    Write-Host "[错误] 未找到虚拟环境。" -ForegroundColor Red
    Write-Host "请先执行 .\scripts\setup_venv.ps1 安装依赖，再运行本脚本。"
    Read-Host "按回车关闭"
    exit 1
}

Write-Host "正在启动 PKUAutoRun（按提示输入）`n" -ForegroundColor Cyan
& $py $main
Write-Host "`n----- 程序已退出 -----" -ForegroundColor Gray
Read-Host "按回车关闭"
