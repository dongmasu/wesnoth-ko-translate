param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Config,
    [Parameter(Position = 1)]
    [string]$Marker
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$version = if ($env:WESNOTH_VERSION) {
    $env:WESNOTH_VERSION
} else {
    (Get-Content -Raw -Encoding UTF8 (Join-Path $root "VERSION")).Trim()
}
$poDate = if ($env:WESNOTH_PO_DATE) {
    $env:WESNOTH_PO_DATE
} else {
    $distDirectory = Join-Path $root "dist"
    $metadata = Get-ChildItem -LiteralPath $distDirectory -Directory -Filter "$version-*" |
        ForEach-Object { Join-Path $_.FullName "ko\PO_LAST_MODIFIED_DATE" } |
        Where-Object { Test-Path -LiteralPath $_ } |
        Sort-Object |
        Select-Object -Last 1
    if ($metadata) {
        (Get-Content -Raw -Encoding UTF8 $metadata).Trim()
    } else {
        $poDirectory = Join-Path $root "work\$version\ko"
        $latestPo = Get-ChildItem -LiteralPath $poDirectory -Filter "*.po" |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 1
        if (-not $latestPo) {
            throw "unable to determine the latest PO modification date"
        }
        $latestPo.LastWriteTime.ToString("yyyyMMdd")
    }
}

if (-not $Marker) {
    $Marker = if ($env:WESNOTH_KO_LOCALE_MARKER) {
        $env:WESNOTH_KO_LOCALE_MARKER
    } else {
        "$version-$poDate"
    }
}

if (-not (Test-Path -LiteralPath $Config -PathType Leaf)) {
    throw "locale config not found: $Config"
}

$content = Get-Content -Raw -Encoding UTF8 $Config
if ($content -notmatch 'name="한국어 \((Hangugeo|[0-9]+\.[0-9]+\.x-[0-9]{8})\)"' -or
    $content -notmatch 'sort_name\s*=\s*"(Hangugeo|[0-9]+\.[0-9]+\.x-[0-9]{8})"') {
    throw "expected Korean locale metadata was not found"
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "$Config.backup-$stamp"
$temporary = "$Config.tmp-$stamp"
Copy-Item -LiteralPath $Config -Destination $backup

$updated = $content -replace 'name="한국어 \([^"]*\)"', "name=""한국어 ($Marker)""" 
$updated = $updated -replace 'sort_name\s*=\s*"[^"]*"', "sort_name = ""$Marker"""
[System.IO.File]::WriteAllText(
    $temporary,
    $updated,
    [System.Text.UTF8Encoding]::new($false)
)
Move-Item -Force -LiteralPath $temporary -Destination $Config

Write-Output "updated: $Config"
Write-Output "backup:  $backup"
Write-Output "label:   한국어 ($Marker)"
