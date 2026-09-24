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

META_DIR="$ROOT/dist/$VERSION/ko"
mkdir -p "$META_DIR"
latest_epoch=0
for po in "$PO_DIR"/*.po; do
    [ -f "$po" ] || continue
    epoch=$(stat -f %m "$po" 2>/dev/null || stat -c %Y "$po")
    if [ "$epoch" -gt "$latest_epoch" ]; then
        latest_epoch=$epoch
    fi
done

if [ -n "${WESNOTH_PO_DATE:-}" ]; then
    po_date=$WESNOTH_PO_DATE
elif [ "$latest_epoch" -gt 0 ]; then
    po_date=$(date -u -r "$latest_epoch" +%Y%m%d 2>/dev/null ||
        date -u -d "@$latest_epoch" +%Y%m%d)
else
    echo "error: unable to determine the latest PO modification date" >&2
    exit 1
fi

printf '%s\n' "$po_date" > "$META_DIR/PO_LAST_MODIFIED_DATE"
echo "MO files written to $OUT_DIR"
echo "last PO modification date recorded in $META_DIR/PO_LAST_MODIFIED_DATE: $po_date"
