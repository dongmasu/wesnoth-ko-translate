#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${1:-${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}}
OUT_DIR=${2:-"$ROOT/dist/$VERSION/ko/LC_MESSAGES"}
PO_DIR="$ROOT/work/$VERSION/ko"

command -v msgfmt >/dev/null 2>&1 || {
    echo "error: msgfmt is not installed" >&2
    exit 1
}

if [ ! -d "$PO_DIR" ]; then
    echo "error: PO directory not found: $PO_DIR" >&2
    exit 1
fi

mkdir -p "$OUT_DIR"
found=0
for po in "$PO_DIR"/*.po; do
    [ -f "$po" ] || continue
    found=1
    name=${po##*/}
    name=${name%.po}
    case "$name" in
        *-ko) domain=${name%-ko} ;;
        *) domain=$name ;;
    esac
    echo "building $domain.mo"
    msgfmt --check -o "$OUT_DIR/$domain.mo" "$po"
done

if [ "$found" -eq 0 ]; then
    echo "error: no PO files found in $PO_DIR" >&2
    exit 1
fi

BUILD_DATE=${WESNOTH_BUILD_DATE:-$(date +%Y%m%d)}
META_DIR="$ROOT/dist/$VERSION/ko"
mkdir -p "$META_DIR"
printf '%s\n' "$BUILD_DATE" > "$META_DIR/MO_BUILD_DATE"
echo "MO files written to $OUT_DIR"
echo "MO build date recorded in $META_DIR/MO_BUILD_DATE: $BUILD_DATE"
