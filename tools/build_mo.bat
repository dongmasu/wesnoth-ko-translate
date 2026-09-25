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

set "PO_TIMESTAMP=%WESNOTH_PO_TIMESTAMP%"
set "PO_DATE=%WESNOTH_PO_DATE%"
if not "%PO_TIMESTAMP%"=="" set "PO_DATE=!PO_TIMESTAMP:~0,4!!PO_TIMESTAMP:~5,2!!PO_TIMESTAMP:~8,2!"
if "%PO_TIMESTAMP%"=="" if not "%PO_DATE%"=="" set "PO_TIMESTAMP=!PO_DATE:~0,4!-!PO_DATE:~4,2!-!PO_DATE:~6,2! 00:00:00+0900"
if "%PO_TIMESTAMP%"=="" for /f "tokens=1,2 delims=|" %%A in ('powershell -NoProfile -Command "$tz=[TimeZoneInfo]::FindSystemTimeZoneById(''Korea Standard Time''); $f=Get-ChildItem -LiteralPath ''%PO_DIR%'' -Filter ''*.po'' | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1; $d=[TimeZoneInfo]::ConvertTimeFromUtc($f.LastWriteTimeUtc,$tz); $ts=$d.ToString(''yyyy-MM-dd HH:mm:ss'') + $d.ToString(''zzz'').Replace('':'',''''); Write-Output ($ts + ''|'' + $d.ToString(''yyyyMMdd''))"') do (
    set "PO_TIMESTAMP=%%A"
    set "PO_DATE=%%B"
)
if "%PO_TIMESTAMP%"=="" (
    echo error: unable to determine the latest PO modification timestamp
    exit /b 1
)
set "DIST_DIR=%ROOT%\dist\%VERSION%-%PO_DATE%"
if "%OUT_DIR%"=="" set "OUT_DIR=%DIST_DIR%\ko\LC_MESSAGES"
set "META_DIR=%DIST_DIR%\ko"
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%META_DIR%" mkdir "%META_DIR%"
set "FOUND=0"
for %%F in ("%PO_DIR%\*.po") do (
    set "FOUND=1"
    set "DOMAIN=%%~nF"
    set "DOMAIN=!DOMAIN:-ko=!"
    echo building !DOMAIN!.mo
    msgfmt --check -o "%OUT_DIR%\!DOMAIN!.mo" "%%~fF"
    if errorlevel 1 exit /b 1
)
if "!FOUND!"=="0" (
    echo error: no PO files found in "%PO_DIR%"
    exit /b 1
)
> "%META_DIR%\PO_LAST_MODIFIED_DATE" echo %PO_TIMESTAMP%
echo MO files written to "%OUT_DIR%"
echo last PO modification timestamp recorded in "%META_DIR%\PO_LAST_MODIFIED_DATE": %PO_TIMESTAMP%
