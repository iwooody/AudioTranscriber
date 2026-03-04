@echo off
echo ========================================
echo AudioTranscriber - 离线录音转写工具
echo ========================================
echo.
echo 正在检查Python环境...

python --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

echo Python已安装
echo.
echo 正在安装依赖...
pip install -r requirements.txt

echo.
echo 启动程序...
python src/main.py

pause
