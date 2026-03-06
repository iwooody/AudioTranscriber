@echo off
chcp 65001 >nul
title AudioTranscriber 安装器
echo ========================================
echo AudioTranscriber - 离线录音转写工具
echo ========================================
echo.
echo 正在检查Python安装...

python --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到Python
    echo.
    echo 请按以下步骤安装Python：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载 Python 3.10 或更高版本
    echo 3. 安装时勾选 "Add Python to PATH"
    echo 4. 安装完成后重新运行此脚本
    echo.
    echo 按任意键打开Python下载页面...
    pause >nul
    start https://www.python.org/downloads/release/python-31011/
    exit /b 1
)

echo Python已安装
echo.
echo 正在安装依赖（这可能需要几分钟）...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo [错误] 依赖安装失败
    echo 请检查网络连接后重试
    pause
    exit /b 1
)

echo.
echo ========================================
echo 安装完成！正在启动程序...
echo ========================================
echo.

python src/main.py

pause
