#!/bin/sh
set -eu

CONFIG=${1:-}
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}
PO_DATE_FILE="$ROOT/dist/$VERSION/ko/PO_LAST_MODIFIED_DATE"
if [ -n "${WESNOTH_PO_DATE:-}" ]; then
    WORK_DATE=$WESNOTH_PO_DATE
elif [ -f "$PO_DATE_FILE" ]; then
    WORK_DATE=$(tr -d '\r\n' < "$PO_DATE_FILE")
else
    echo "error: PO modification date not found; run tools/build_mo.sh first" >&2
    exit 1
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
