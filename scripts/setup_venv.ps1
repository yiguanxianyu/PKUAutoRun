# 在项目根目录创建 venv 并安装 requirements.txt（需已安装 Python 3）
$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv (Join-Path $ProjectRoot "venv")
    } else {
        python -m venv (Join-Path $ProjectRoot "venv")
    }
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt") -i "https://pypi.tuna.tsinghua.edu.cn/simple"

Write-Host ""
Write-Host "完成。请直接双击项目根目录的 run.bat，或在根目录执行: .\run.ps1"
