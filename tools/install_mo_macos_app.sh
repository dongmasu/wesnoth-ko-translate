#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}
SOURCE_APP=${1:-"$HOME/Downloads/The Battle for Wesnoth.app"}
TARGET_APP=${2:-"$HOME/Applications/Wesnoth-$VERSION-unsigned.app"}
CONFIG_SOURCE=${3:-"$ROOT/work/$VERSION/ko_KR.cfg"}

case "$TARGET_APP" in
    *-unsigned.app) ;;
    *)
        echo "error: target app must end with -unsigned.app: $TARGET_APP" >&2
        exit 1
        ;;
esac

if [ -e "$TARGET_APP" ]; then
    if [ ! -d "$TARGET_APP/Contents/Resources" ]; then
        echo "error: existing target is not a Wesnoth app: $TARGET_APP" >&2
        exit 1
    fi
    echo "updating existing unsigned app: $TARGET_APP"
else
    if [ ! -d "$SOURCE_APP/Contents/Resources" ]; then
        echo "error: source Wesnoth app not found: $SOURCE_APP" >&2
        exit 1
    fi
    mkdir -p "$(dirname "$TARGET_APP")"
    ditto --noqtn --noextattr "$SOURCE_APP" "$TARGET_APP"

    # Remove the distributor signature before changing bundled resources.
    codesign --remove-signature "$TARGET_APP"
    echo "created unsigned app copy: $TARGET_APP"
fi

if [ ! -f "$CONFIG_SOURCE" ]; then
    echo "error: ko_KR.cfg not found: $CONFIG_SOURCE" >&2
    exit 1
fi

mkdir -p \
    "$TARGET_APP/Contents/Resources/data/languages" \
    "$TARGET_APP/Contents/Resources/translations/ko/LC_MESSAGES"
"$ROOT/tools/install_mo.sh" \
    "$TARGET_APP/Contents/Resources/translations/ko/LC_MESSAGES"
cp "$CONFIG_SOURCE" \
    "$TARGET_APP/Contents/Resources/data/languages/ko_KR.cfg"
codesign --force --deep --sign - "$TARGET_APP"
codesign --verify --deep --strict "$TARGET_APP"

echo "installed Korean translation app: $TARGET_APP"
echo "launch with: open \"$TARGET_APP\""
