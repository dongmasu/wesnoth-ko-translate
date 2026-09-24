#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${WESNOTH_VERSION:-$(tr -d '\r\n' < "$ROOT/VERSION")}
SOURCE_APP=${1:-"$HOME/Downloads/The Battle for Wesnoth.app"}
TARGET_APP=${2:-"$HOME/Applications/Wesnoth-$VERSION-ko.app"}

if [ ! -d "$SOURCE_APP/Contents/Resources" ]; then
    echo "error: source Wesnoth app not found: $SOURCE_APP" >&2
    exit 1
fi

if [ -e "$TARGET_APP" ]; then
    echo "error: target already exists; choose another path or remove it first: $TARGET_APP" >&2
    exit 1
fi

mkdir -p "$(dirname "$TARGET_APP")"
ditto --noqtn --noextattr "$SOURCE_APP" "$TARGET_APP"

# Remove the distributor signature before changing bundled MO resources.
codesign --remove-signature "$TARGET_APP"
"$ROOT/tools/install_mo.sh" \
    "$TARGET_APP/Contents/Resources/translations/ko/LC_MESSAGES"
codesign --force --deep --sign - "$TARGET_APP"
codesign --verify --deep --strict "$TARGET_APP"

echo "installed signed-local MO app: $TARGET_APP"
echo "launch with: open \"$TARGET_APP\""
