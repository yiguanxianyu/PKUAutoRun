@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "PY=%~dp0venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [错误] 未找到虚拟环境。
  echo 请先双击 scripts\setup_venv.bat 完成安装，再双击本文件运行。
  pause
  exit /b 1
)

title PKUAutoRun
echo 正在启动 PKUAutoRun（按提示输入；请勿提前关闭本窗口）
echo.
"%PY%" "%~dp0main.py"
echo.
echo ----- 程序已退出 -----
pause
