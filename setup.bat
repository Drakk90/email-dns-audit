@echo off
setlocal
cd /d "%~dp0"
title Email DNS Audit Neon - Windows Installer
echo.
echo Launching automated setup via PowerShell...
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Setup encountered an issue. Review the messages above.
)
echo.
pause
