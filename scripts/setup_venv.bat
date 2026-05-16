@echo off
chcp 65001 >nul
cd /d "%~dp0.."

if exist "venv\Scripts\python.exe" goto install

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m venv venv
) else (
  python -m venv venv
)
if errorlevel 1 (
  echo 未找到 Python，请先安装 Python 3 并勾选 "Add to PATH"
  pause
  exit /b 1
)

:install
call "venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
  echo 依赖安装失败
  pause
  exit /b 1
)

echo.
echo 完成。下次请直接双击项目根目录的 run.bat 启动程序。
pause
