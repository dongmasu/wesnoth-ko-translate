@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "VERSION=%VERSION%"
if "%VERSION%"=="" set "VERSION=1.18.x"
set "TARGET_DIR=%~1"
set "SOURCE_DIR=%~2"
if "%SOURCE_DIR%"=="" set "SOURCE_DIR=%ROOT%\dist\%VERSION%\ko\LC_MESSAGES"

if "%TARGET_DIR%"=="" (
    echo usage: %~nx0 ^<game translations\ko\LC_MESSAGES^> [source mo directory]
    exit /b 2
)
if not exist "%SOURCE_DIR%" (
    echo error: MO directory not found: "%SOURCE_DIR%"
    echo run build_mo.bat first
    exit /b 1
)

dir /b "%SOURCE_DIR%\*.mo" >nul 2>nul
if errorlevel 1 (
    echo error: no MO files found in "%SOURCE_DIR%"
    exit /b 1
)
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

dir /b "%TARGET_DIR%\*.mo" >nul 2>nul
if not errorlevel 1 (
    for /f "usebackq delims=" %%T in (`powershell -NoProfile -Command "(Get-Date).ToString('yyyyMMdd-HHmmss')"`) do set "STAMP=%%T"
    set "BACKUP=%TARGET_DIR%.backup-!STAMP!"
    mkdir "!BACKUP!"
    copy /y "%TARGET_DIR%\*.mo" "!BACKUP!\" >nul
    echo backed up existing MO files to "!BACKUP!"
)

copy /y "%SOURCE_DIR%\*.mo" "%TARGET_DIR%\" >nul
if errorlevel 1 exit /b 1
echo installed MO files into "%TARGET_DIR%"
