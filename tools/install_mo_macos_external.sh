#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
APP=${1:-"$HOME/Downloads/The Battle for Wesnoth.app"}
DATA_DIR=${2:-"$HOME/Applications/Wesnoth-1.18.8-data"}

if [ ! -d "$APP/Contents/Resources" ]; then
    echo "error: Wesnoth app resources not found: $APP" >&2
    exit 1
fi

mkdir -p "$DATA_DIR"
ditto "$APP/Contents/Resources/" "$DATA_DIR/"
"$ROOT/tools/install_mo.sh" "$DATA_DIR/translations/ko/LC_MESSAGES"

echo "external data directory: $DATA_DIR"
echo "launch with:"
echo "open \"$APP\" --args \"--data-dir=$DATA_DIR\""
