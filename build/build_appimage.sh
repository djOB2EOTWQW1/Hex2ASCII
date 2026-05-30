#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPDIR="$(mktemp -d)/Hex2ASCII.AppDir"
mkdir -p "$APPDIR/usr/share/hex2ascii" "$APPDIR/usr/bin"

cp -r "$ROOT/app.py" "$ROOT/core" "$ROOT/gui_qt" "$ROOT/gui_ctk" \
    "$APPDIR/usr/share/hex2ascii/"
install -m755 "$ROOT/build/AppRun" "$APPDIR/AppRun"
cp "$ROOT/build/hex2ascii.desktop" "$APPDIR/hex2ascii.desktop"
cp "${ROOT}/build/hex2ascii.png" "$APPDIR/hex2ascii.png" 2>/dev/null || \
    printf '' > "$APPDIR/hex2ascii.png"

if ! command -v appimagetool >/dev/null; then
    curl -L -o /tmp/appimagetool \
        https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x /tmp/appimagetool
    APPIMAGETOOL=/tmp/appimagetool
else
    APPIMAGETOOL=appimagetool
fi

ARCH=x86_64 "$APPIMAGETOOL" --appimage-extract-and-run "$APPDIR" \
    "$ROOT/Hex2ASCII-x86_64.AppImage"
echo "Built Hex2ASCII-x86_64.AppImage"
