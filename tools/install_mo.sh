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
    po_timestamp=$(TZ=Asia/Seoul date -r "$latest_epoch" '+%Y-%m-%d %H:%M:%S%z' 2>/dev/null ||
        TZ=Asia/Seoul date -d "@$latest_epoch" '+%Y-%m-%d %H:%M:%S%z')
fi

if [ -z "${po_timestamp:-}" ]; then
    metadata_file=$(find "$ROOT/dist" -type f \
        -path "$ROOT/dist/$VERSION-"'*'/ko/PO_LAST_MODIFIED_DATE \
        2>/dev/null | sort | tail -n 1)
    if [ -n "$metadata_file" ]; then
        po_timestamp=$(tr -d '\r\n' < "$metadata_file")
    fi
fi
case "$po_timestamp" in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]+0900)
        ;;
    [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])
        po_year=${po_timestamp%????}
        po_month_day=${po_timestamp#????}
        po_month=${po_month_day%??}
        po_day=${po_month_day#??}
        po_timestamp="$po_year-$po_month-$po_day 00:00:00+0900"
        ;;
    *)
        echo "error: PO timestamp must be YYYY-MM-DD HH:MM:SS+0900" >&2
        exit 1
        ;;
esac
po_date=$(printf '%s' "$po_timestamp" | cut -c1-10 | tr -d '-')
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
for mo in "$TARGET_DIR"/*.mo; do
    [ -f "$mo" ] || continue
    rm -f "$mo"
done
cp "$SOURCE_DIR"/*.mo "$TARGET_DIR"/
echo "synchronized MO files into $TARGET_DIR"
