@echo off
setlocal
cd /d "%~dp0"

:: 设置 Playwright 浏览器路径到 H 盘
set "PLAYWRIGHT_BROWSERS_PATH=%~dp0.playwright-browsers"

:: 检查是否安装了虚拟环境
if not exist ".venv" (
    echo [错误] 未发现虚拟环境，请先运行 setup_h_drive.ps1
    pause
    exit /b 1
)

:: 将虚拟环境的 Scripts 目录加入 PATH，以便 api/main.py 能找到 uv
set "PATH=%~dp0.venv\Scripts;%PATH%"

echo 正在启动 MediaCrawler 可视化界面...
echo 请在浏览器中访问: http://localhost:8080
echo.

:: 启动 API 服务
".venv\Scripts\python.exe" -m api.main

pause
