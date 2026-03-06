@echo off
chcp 65001 >nul
title AudioTranscriber 便携版安装器
echo ========================================
echo AudioTranscriber - 便携版
echo ========================================
echo.
echo 正在下载Python便携版...
echo.

:: 创建下载目录
mkdir "%TEMP%\WinPython" 2>nul

:: 下载Python便携版（精简版）
echo 正在下载，请稍等...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/winpython/winpython/releases/download/6.4.20230625final/Winpython64-3.10.11.1dot.exe' -OutFile '%TEMP%\WinPython\wp.exe'"

if not exist "%TEMP%\WinPython\wp.exe" (
    echo 下载失败，请手动下载：
    echo https://github.com/winpython/winpython/releases/
    pause
    exit /b 1
)

echo.
echo 正在解压Python便携版...
"%TEMP%\WinPython\wp.exe" -y -o"%CD%\python"

echo.
echo 正在安装依赖...
"%CD%\python\WPy64-31110\python.exe" -m pip install -r requirements.txt

echo.
echo 正在创建启动快捷方式...
echo @echo off > "启动AudioTranscriber.bat"
echo chcp 65001 >nul >> "启动AudioTranscriber.bat"
echo "%~dp0python\WPy64-31110\python.exe" src/main.py >> "启动AudioTranscriber.bat"
echo pause >> "启动AudioTranscriber.bat"

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 现在可以双击 "启动AudioTranscriber.bat" 运行程序
echo.
pause
