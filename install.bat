@echo off
chcp 65001 >nul
echo ============================================
echo VideoCut CLI 安装程序
echo ============================================
echo.

REM 获取当前目录
set "INSTALL_DIR=%CD%"

REM 创建 videocut.bat 文件
echo 正在创建启动脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo python "%INSTALL_DIR%\video_subtitle_translator\cli.py" %%*
) > "%INSTALL_DIR%\videocut.bat"

echo ✓ 启动脚本已创建: %INSTALL_DIR%\videocut.bat
echo.

REM 添加到用户PATH
echo 正在添加到系统环境变量...
echo.

REM 使用PowerShell添加到用户PATH
powershell -Command "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($path -notlike '*%INSTALL_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $path + ';%INSTALL_DIR%', 'User'); Write-Host '✓ 已添加到用户PATH' } else { Write-Host '✓ 已存在于PATH中' }"

echo.
echo ============================================
echo 安装完成！
echo ============================================
echo.
echo 使用方法:
echo   videocut "视频路径.mp4"
echo.
echo 示例:
echo   videocut "D:\videos\lecture.mp4"
echo   videocut "D:\videos\lecture.mp4" -o "output.mp4"
echo.
echo 注意: 请重新打开命令行窗口以使环境变量生效
echo.
pause
