#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${VERSION:-${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}}
SOURCE_DIR=${2:-"$ROOT/dist/$VERSION/ko/LC_MESSAGES"}
TARGET_DIR=${1:-}

if [ -z "$TARGET_DIR" ]; then
    echo "usage: $0 <game translations/ko/LC_MESSAGES> [source mo directory]" >&2
    exit 2
fi

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
backup_root=${WESNOTH_BACKUP_DIR:-"$ROOT/dist/$VERSION/ko"}
backup="$backup_root/LC_MESSAGES.backup-$(date +%Y%m%d-%H%M%S)"
existing=0
for mo in "$TARGET_DIR"/*.mo; do
    if [ -f "$mo" ]; then
        existing=1
        break
    fi
done
if [ "$existing" -eq 1 ]; then
    mkdir -p "$backup"
    cp "$TARGET_DIR"/*.mo "$backup"/
    echo "backed up existing MO files to $backup"
fi

cp "$SOURCE_DIR"/*.mo "$TARGET_DIR"/
echo "installed MO files into $TARGET_DIR"
