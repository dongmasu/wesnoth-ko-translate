@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0.."
set "VERSION=%VERSION%"
if "%VERSION%"=="" set "VERSION=%WESNOTH_VERSION%"
if "%VERSION%"=="" for /f "usebackq delims=" %%V in ("%ROOT%\VERSION") do set "VERSION=%%V"
set "TARGET_DIR=%~1"
set "SOURCE_DIR=%~2"
set "PO_DIR=%ROOT%\work\%VERSION%\ko"
set "PO_DATE=%WESNOTH_PO_DATE%"
if "%PO_DATE%"=="" for /f %%D in ('powershell -NoProfile -Command "$tz=[TimeZoneInfo]::FindSystemTimeZoneById(''Korea Standard Time''); $f=Get-ChildItem -LiteralPath ''%PO_DIR%'' -Filter ''*.po'' | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1; [TimeZoneInfo]::ConvertTimeFromUtc($f.LastWriteTimeUtc,$tz).ToString(''yyyyMMdd'')"') do set "PO_DATE=%%D"
set "DIST_DIR=%ROOT%\dist\%VERSION%-%PO_DATE%"
if "%SOURCE_DIR%"=="" set "SOURCE_DIR=%DIST_DIR%\ko\LC_MESSAGES"

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

del /q "%TARGET_DIR%\*.mo" >nul 2>nul
copy /y "%SOURCE_DIR%\*.mo" "%TARGET_DIR%\" >nul
if errorlevel 1 exit /b 1
echo synchronized MO files into "%TARGET_DIR%"
