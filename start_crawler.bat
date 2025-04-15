@echo off
echo ===================================
echo    E-Hentai画廊下载器启动脚本
echo ===================================
echo.

:: 检查Python是否已安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python安装。请先安装Python 3.6或更高版本。
    echo 您可以从 https://www.python.org/downloads/ 下载Python。
    echo.
    echo 或者运行install_dependencies.bat安装所需依赖。
    echo.
    pause
    exit /b 1
)

:: 检查必要的Python库
echo 正在检查必要的Python库...
python -c "import requests, bs4" >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 缺少必要的Python库。
    echo 正在尝试安装必要的库...
    pip install requests beautifulsoup4
    if %errorlevel% neq 0 (
        echo [错误] 安装库失败。请手动运行以下命令：
        echo pip install requests beautifulsoup4
        echo.
        pause
        exit /b 1
    )
    echo 库安装成功！
)

echo 正在启动E-Hentai画廊下载器...
echo.

:: 启动Python脚本
python app.py

echo.
echo 程序已结束运行。
pause