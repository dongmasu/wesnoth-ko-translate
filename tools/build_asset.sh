#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${1:-${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}}
PO_DATE=${2:-}
CONFIG_SOURCE=${3:-}

if [ -z "$PO_DATE" ]; then
    metadata=$(find "$ROOT/dist" -type f \
        -path "$ROOT/dist/$VERSION-"'*'/ko/PO_LAST_MODIFIED_DATE \
        2>/dev/null | sort | tail -n 1)
    [ -n "$metadata" ] || {
        echo "error: PO_LAST_MODIFIED_DATE not found" >&2
        exit 1
    }
    PO_DATE=$(tr -d '\r\n' < "$metadata" | cut -c1-10 | tr -d '-')
fi

case "$PO_DATE" in
    [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]) ;;
    *)
        echo "error: PO_DATE must be YYYYMMDD" >&2
        exit 1
        ;;
esac

DIST_DIR="$ROOT/dist/$VERSION-$PO_DATE"
MO_DIR="$DIST_DIR/ko/LC_MESSAGES"
[ -d "$MO_DIR" ] || {
    echo "error: MO directory not found: $MO_DIR" >&2
    echo "run tools/build_mo.sh first" >&2
    exit 1
}

if [ -z "$CONFIG_SOURCE" ]; then
    CONFIG_SOURCE=${WESNOTH_KO_CONFIG:-}
fi
if [ -z "$CONFIG_SOURCE" ] || [ ! -f "$CONFIG_SOURCE" ]; then
    echo "error: pass ko_KR.cfg as the third argument" >&2
    exit 1
fi

ASSET_NAME="wesnoth-ko-translate-$VERSION-$PO_DATE"
ASSET="$DIST_DIR/$ASSET_NAME.zip"
STAGE=$(mktemp -d "${TMPDIR:-/tmp}/wesnoth-ko-asset.XXXXXX")
trap 'rm -rf "$STAGE"' EXIT HUP INT TERM

mkdir -p \
    "$STAGE/data/languages" \
    "$STAGE/translations/ko/LC_MESSAGES"
cp "$CONFIG_SOURCE" "$STAGE/data/languages/ko_KR.cfg"
cp "$MO_DIR"/*.mo "$STAGE/translations/ko/LC_MESSAGES/"
cp "$ROOT/README.md" "$ROOT/INSTALL.md" "$ROOT/VERSION" "$STAGE/"

cat > "$STAGE/install.sh" <<'SCRIPT'
#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TARGET=${1:-}
[ -n "$TARGET" ] || {
    echo "usage: $0 <Wesnoth game root or app Resources directory>" >&2
    exit 2
}

if [ -d "$TARGET/Contents/Resources" ]; then
    TARGET="$TARGET/Contents/Resources"
fi
[ -d "$TARGET" ] || {
    echo "error: target directory not found: $TARGET" >&2
    exit 1
}

mkdir -p "$TARGET/data/languages"
if [ -d "$TARGET/data/translations" ]; then
    TRANSLATIONS="$TARGET/data/translations"
else
    TRANSLATIONS="$TARGET/translations"
fi
mkdir -p "$TRANSLATIONS/ko/LC_MESSAGES"
cp "$ROOT/data/languages/ko_KR.cfg" "$TARGET/data/languages/ko_KR.cfg"
rm -f "$TRANSLATIONS/ko/LC_MESSAGES/"*.mo
cp "$ROOT/translations/ko/LC_MESSAGES/"*.mo "$TRANSLATIONS/ko/LC_MESSAGES/"
echo "installed Wesnoth Korean translation into $TARGET"
SCRIPT
chmod +x "$STAGE/install.sh"

cat > "$STAGE/install.bat" <<'SCRIPT'
@echo off
setlocal
set "ROOT=%~dp0"
set "TARGET=%~1"
if "%TARGET%"=="" (
  echo Usage: install.bat "Wesnoth game directory"
  exit /b 2
)
if not exist "%TARGET%\data\languages" mkdir "%TARGET%\data\languages"
if exist "%TARGET%\data\translations" (
  set "TRANSLATIONS=%TARGET%\data\translations"
) else (
  set "TRANSLATIONS=%TARGET%\translations"
)
if not exist "%TRANSLATIONS%\ko\LC_MESSAGES" mkdir "%TRANSLATIONS%\ko\LC_MESSAGES"
copy /Y "%ROOT%data\languages\ko_KR.cfg" "%TARGET%\data\languages\ko_KR.cfg" >NUL
del /Q "%TRANSLATIONS%\ko\LC_MESSAGES\*.mo" 2>NUL
copy /Y "%ROOT%translations\ko\LC_MESSAGES\*.mo" "%TRANSLATIONS%\ko\LC_MESSAGES\" >NUL
echo Installed Wesnoth Korean translation into %TARGET%
endlocal
SCRIPT

mkdir -p "$DIST_DIR"
rm -f "$ASSET"
(cd "$STAGE" && zip -qr "$ASSET" .)
echo "asset written to $ASSET"
