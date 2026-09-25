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

if [ -n "${WESNOTH_PO_TIMESTAMP:-}" ]; then
    po_timestamp=$WESNOTH_PO_TIMESTAMP
elif [ -n "${WESNOTH_PO_DATE:-}" ]; then
    case "$WESNOTH_PO_DATE" in
        [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])
            po_year=${WESNOTH_PO_DATE%????}
            po_month_day=${WESNOTH_PO_DATE#????}
            po_month=${po_month_day%??}
            po_day=${po_month_day#??}
            po_timestamp="$po_year-$po_month-$po_day 00:00:00+0900"
            ;;
        *)
            echo "error: WESNOTH_PO_DATE must be YYYYMMDD" >&2
            exit 1
            ;;
    esac
elif [ "$latest_epoch" -gt 0 ]; then
    po_timestamp=$(TZ=Asia/Seoul date -r "$latest_epoch" '+%Y-%m-%d %H:%M:%S%z' 2>/dev/null ||
        TZ=Asia/Seoul date -d "@$latest_epoch" '+%Y-%m-%d %H:%M:%S%z')
else
    echo "error: unable to determine the latest PO modification date" >&2
    exit 1
fi

case "$po_timestamp" in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]+0900)
        ;;
    *)
        echo "error: PO timestamp must be YYYY-MM-DD HH:MM:SS+0900" >&2
        exit 1
        ;;
esac
po_date=$(printf '%s' "$po_timestamp" | cut -c1-10 | tr -d '-')
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

printf '%s\n' "$po_timestamp" > "$META_DIR/PO_LAST_MODIFIED_DATE"
echo "MO files written to $OUT_DIR"
echo "last PO modification timestamp recorded in $META_DIR/PO_LAST_MODIFIED_DATE: $po_timestamp"
