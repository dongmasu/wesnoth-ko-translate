@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "VERSION=%~1"
if "%VERSION%"=="" set "VERSION=%WESNOTH_VERSION%"
if "%VERSION%"=="" for /f "usebackq delims=" %%V in ("%ROOT%\VERSION") do set "VERSION=%%V"
set "OUT_DIR=%~2"
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
set "PO_DATE=%WESNOTH_PO_DATE%"
if "%PO_DATE%"=="" for /f %%D in ('powershell -NoProfile -Command "$tz=[TimeZoneInfo]::FindSystemTimeZoneById(''Korea Standard Time''); $f=Get-ChildItem -LiteralPath ''%PO_DIR%'' -Filter ''*.po'' | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1; [TimeZoneInfo]::ConvertTimeFromUtc($f.LastWriteTimeUtc,$tz).ToString(''yyyyMMdd'')"') do set "PO_DATE=%%D"
if "%PO_DATE%"=="" (
    echo error: unable to determine the latest PO modification date
    exit /b 1
)
set "DIST_DIR=%ROOT%\dist\%VERSION%-%PO_DATE%"
if "%OUT_DIR%"=="" set "OUT_DIR=%DIST_DIR%\ko\LC_MESSAGES"
set "META_DIR=%DIST_DIR%\ko"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%META_DIR%" mkdir "%META_DIR%"
> "%META_DIR%\PO_LAST_MODIFIED_DATE" echo %PO_DATE%
echo MO files written to "%OUT_DIR%"
echo last PO modification date recorded in "%META_DIR%\PO_LAST_MODIFIED_DATE": %PO_DATE%
