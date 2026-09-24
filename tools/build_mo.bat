@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "VERSION=%~1"
if "%VERSION%"=="" set "VERSION=%WESNOTH_VERSION%"
if "%VERSION%"=="" for /f "usebackq delims=" %%V in ("%ROOT%\VERSION") do set "VERSION=%%V"
set "OUT_DIR=%~2"
if "%OUT_DIR%"=="" set "OUT_DIR=%ROOT%\dist\%VERSION%\ko\LC_MESSAGES"
set "PO_DIR=%ROOT%\work\%VERSION%\ko"

where msgfmt >nul 2>nul
if errorlevel 1 (
    echo error: msgfmt is not installed
    exit /b 1
)
if not exist "%PO_DIR%" (
    echo error: PO directory not found: "%PO_DIR%"
    exit /b 1
)

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
set "FOUND=0"
for %%F in ("%PO_DIR%\*.po") do (
    set "FOUND=1"
    set "DOMAIN=%%~nF"
    set "DOMAIN=!DOMAIN:-ko=!"
    echo building !DOMAIN!.mo
    msgfmt --check -o "%OUT_DIR%\!DOMAIN!.mo" "%%~fF"
    if errorlevel 1 exit /b 1
)

if "%FOUND%"=="0" (
    echo error: no PO files found in "%PO_DIR%"
    exit /b 1
)
echo MO files written to "%OUT_DIR%"
