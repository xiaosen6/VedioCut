@echo off
chcp 65001 >nul
echo ============================================
echo VideoCut CLI Installer
echo ============================================
echo.

REM Get current directory
set "INSTALL_DIR=%CD%"

REM Create videocut.bat
(
echo @echo off
echo chcp 65001 ^>nul
echo python "%INSTALL_DIR%\video_subtitle_translator\cli.py" %%*
) > "%INSTALL_DIR%\videocut.bat"

echo [OK] videocut.bat created
echo.

REM Add to PATH
powershell -Command "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($path -notlike '*%INSTALL_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $path + ';%INSTALL_DIR%', 'User'); Write-Host '[OK] Added to PATH' } else { Write-Host '[OK] Already in PATH' }"

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Usage: videocut "video.mp4"
echo.
echo Note: Please restart command prompt
echo.
pause
