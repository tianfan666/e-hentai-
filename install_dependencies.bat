@echo off
echo ===================================
echo E-Hentai画廊下载器 - 依赖库安装工具
echo ===================================
echo.

:: 检查Python是否已安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python安装。请先安装Python 3.6或更高版本。
    echo 您可以从 https://www.python.org/downloads/ 下载Python。
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
echo [信息] 检测到Python安装:
python --version
echo.

:: 安装依赖库
echo [信息] 开始安装依赖库...
echo.

echo [1/2] 安装 requests 库...
pip install requests
if %errorlevel% neq 0 (
    echo [警告] requests 库安装失败，尝试使用其他方法...
    python -m pip install requests
)

echo.
echo [2/2] 安装 beautifulsoup4 库...
pip install beautifulsoup4
if %errorlevel% neq 0 (
    echo [警告] beautifulsoup4 库安装失败，尝试使用其他方法...
    python -m pip install beautifulsoup4
)

echo.
echo [信息] 检查安装结果...

python -c "import requests; import bs4; print('[成功] 所有依赖库已成功安装！')" 2>nul
if %errorlevel% neq 0 (
    echo [错误] 依赖库安装可能不完整，请检查上述错误信息。
) else (
    echo [信息] 现在您可以运行 app.py 来使用E-Hentai画廊下载器了。
)

echo.
echo 按任意键退出...
pause > nul