@echo off
setlocal
cd /d "%~dp0"
title Email DNS Audit Neon - Audit Runner
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Execution encountered an issue. Review the messages above.
)
echo.
pause
