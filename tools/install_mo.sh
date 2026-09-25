#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${VERSION:-${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}}
PO_DIR="$ROOT/work/$VERSION/ko"
TARGET_DIR=${1:-}

if [ -z "$TARGET_DIR" ]; then
    echo "usage: $0 <game translations/ko/LC_MESSAGES> [source mo directory]" >&2
    exit 2
fi

if [ -n "${WESNOTH_PO_DATE:-}" ]; then
    po_date=$WESNOTH_PO_DATE
else
    latest_epoch=0
    for po in "$PO_DIR"/*.po; do
        [ -f "$po" ] || continue
        epoch=$(stat -f %m "$po" 2>/dev/null || true)
        case "$epoch" in
            ''|*[!0-9]*) epoch=$(stat -c %Y "$po") ;;
        esac
        if [ "$epoch" -gt "$latest_epoch" ]; then
            latest_epoch=$epoch
        fi
    done
    if [ "$latest_epoch" -le 0 ]; then
        echo "error: unable to determine the latest PO modification date" >&2
        exit 1
    fi
    po_date=$(TZ=Asia/Seoul date -r "$latest_epoch" +%Y%m%d 2>/dev/null ||
        TZ=Asia/Seoul date -d "@$latest_epoch" +%Y%m%d)
fi

SOURCE_DIR=${2:-"$ROOT/dist/$VERSION-$po_date/ko/LC_MESSAGES"}
if [ ! -d "$SOURCE_DIR" ]; then
    echo "error: MO directory not found: $SOURCE_DIR" >&2
    echo "run tools/build_mo.sh first" >&2
    exit 1
fi

set -- "$SOURCE_DIR"/*.mo
[ -f "$1" ] || {
    echo "error: no MO files found in $SOURCE_DIR" >&2
    exit 1
}

mkdir -p "$TARGET_DIR"
cp "$SOURCE_DIR"/*.mo "$TARGET_DIR"/
echo "installed MO files into $TARGET_DIR"
