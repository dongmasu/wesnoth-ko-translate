#!/bin/sh
set -eu

CONFIG=${1:-}
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}
if [ -n "${WESNOTH_PO_DATE:-}" ]; then
    WORK_DATE=$WESNOTH_PO_DATE
else
    PO_DATE_FILE=$(find "$ROOT/dist" -type f \
        -path "$ROOT/dist/$VERSION-"'*'"'/ko/PO_LAST_MODIFIED_DATE' \
        2>/dev/null | sort | tail -n 1)
    if [ -n "$PO_DATE_FILE" ]; then
        WORK_DATE=$(tr -d '\r\n' < "$PO_DATE_FILE")
    else
        latest_epoch=0
        for po in "$ROOT/work/$VERSION/ko"/*.po; do
            [ -f "$po" ] || continue
            epoch=$(stat -f %m "$po" 2>/dev/null || true)
            case "$epoch" in
                ''|*[!0-9]*) epoch=$(stat -c %Y "$po") ;;
            esac
            if [ "$epoch" -gt "$latest_epoch" ]; then
                latest_epoch=$epoch
            fi
        done
        [ "$latest_epoch" -gt 0 ] || {
            echo "error: PO modification date not found" >&2
            exit 1
        }
        WORK_DATE=$(TZ=Asia/Seoul date -r "$latest_epoch" +%Y%m%d 2>/dev/null ||
            TZ=Asia/Seoul date -d "@$latest_epoch" +%Y%m%d)
    fi
fi
MARKER=${2:-${WESNOTH_KO_LOCALE_MARKER:-${VERSION}-${WORK_DATE}}}

if [ -z "$CONFIG" ]; then
    echo "usage: $0 /path/to/data/languages/ko_KR.cfg [marker]" >&2
    exit 2
fi

if [ ! -f "$CONFIG" ]; then
    echo "error: locale config not found: $CONFIG" >&2
    exit 1
fi

case "$MARKER" in
    *'
'*|'')
        echo "error: marker must be a non-empty single-line value" >&2
        exit 2
        ;;
esac

if ! grep -Eq 'name="한국어 \((Hangugeo|[0-9]+\.[0-9]+\.x-[0-9]{8})\)"' "$CONFIG" ||
   ! grep -Eq 'sort_name = "(Hangugeo|[0-9]+\.[0-9]+\.x-[0-9]{8})"' "$CONFIG"; then
    echo "error: expected Korean locale metadata was not found" >&2
    exit 1
fi

STAMP=$(date +%Y%m%d-%H%M%S)
BACKUP="${CONFIG}.backup-${STAMP}"
TMP="${CONFIG}.tmp-${STAMP}"
cp "$CONFIG" "$BACKUP"

awk -v marker="$MARKER" '
    /name="한국어 \([^"]*\)"/ {
        sub(/name="한국어 \([^"]*\)"/, "name=\"한국어 (" marker ")\"")
    }
    /sort_name = "[^"]*"/ {
        sub(/sort_name = "[^"]*"/, "sort_name = \"" marker "\"")
    }
    { print }
' "$CONFIG" > "$TMP"
mv "$TMP" "$CONFIG"

echo "updated: $CONFIG"
echo "backup:  $BACKUP"
echo "label:   한국어 ($MARKER)"
