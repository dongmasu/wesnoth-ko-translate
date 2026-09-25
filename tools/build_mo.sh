#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${1:-${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}}
OUTPUT_DIR_ARG=${2:-}
PO_DIR="$ROOT/work/$VERSION/ko"

command -v msgfmt >/dev/null 2>&1 || {
    echo "error: msgfmt is not installed" >&2
    exit 1
}

if [ ! -d "$PO_DIR" ]; then
    echo "error: PO directory not found: $PO_DIR" >&2
    exit 1
fi

found=0
for po in "$PO_DIR"/*.po; do
    [ -f "$po" ] || continue
    found=1
done
if [ "$found" -eq 0 ]; then
    echo "error: no PO files found in $PO_DIR" >&2
    exit 1
fi

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

if [ -n "${WESNOTH_PO_DATE:-}" ]; then
    po_date=$WESNOTH_PO_DATE
elif [ "$latest_epoch" -gt 0 ]; then
    po_date=$(TZ=Asia/Seoul date -r "$latest_epoch" +%Y%m%d 2>/dev/null ||
        TZ=Asia/Seoul date -d "@$latest_epoch" +%Y%m%d)
else
    echo "error: unable to determine the latest PO modification date" >&2
    exit 1
fi

DIST_DIR="$ROOT/dist/$VERSION-$po_date"
OUT_DIR=${OUTPUT_DIR_ARG:-"$DIST_DIR/ko/LC_MESSAGES"}
META_DIR="$DIST_DIR/ko"
mkdir -p "$OUT_DIR" "$META_DIR"
for po in "$PO_DIR"/*.po; do
    name=${po##*/}
    name=${name%.po}
    case "$name" in
        *-ko) domain=${name%-ko} ;;
        *) domain=$name ;;
    esac
    echo "building $domain.mo"
    msgfmt --check -o "$OUT_DIR/$domain.mo" "$po"
done

printf '%s\n' "$po_date" > "$META_DIR/PO_LAST_MODIFIED_DATE"
echo "MO files written to $OUT_DIR"
echo "last PO modification date recorded in $META_DIR/PO_LAST_MODIFIED_DATE: $po_date"
