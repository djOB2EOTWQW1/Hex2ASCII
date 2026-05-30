#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PKG="$(mktemp -d)/hex2ascii"
mkdir -p "$PKG/DEBIAN" "$PKG/usr/share/hex2ascii" "$PKG/usr/bin" \
    "$PKG/usr/share/applications"

cp "$ROOT/build/debian/control" "$PKG/DEBIAN/control"
cp -r "$ROOT/app.py" "$ROOT/core" "$ROOT/gui_qt" "$ROOT/gui_ctk" \
    "$PKG/usr/share/hex2ascii/"
cp "$ROOT/build/hex2ascii.desktop" "$PKG/usr/share/applications/hex2ascii.desktop"
cat > "$PKG/usr/bin/hex2ascii" <<'EOF'
#!/bin/sh
exec python3 /usr/share/hex2ascii/app.py --backend qt "$@"
EOF
chmod 755 "$PKG/usr/bin/hex2ascii"

dpkg-deb --build --root-owner-group "$PKG" "$ROOT/hex2ascii_2.0.0_all.deb"
echo "Built hex2ascii_2.0.0_all.deb"
