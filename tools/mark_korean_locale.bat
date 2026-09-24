@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0mark_korean_locale.ps1" %*
exit /b %errorlevel%
