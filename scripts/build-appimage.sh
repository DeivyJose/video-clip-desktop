#!/usr/bin/env bash

set -euo pipefail


# =========================================================
# VIDEOCLIP DESKTOP - APPIMAGE BUILD
# =========================================================


PROJECT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

cd "$PROJECT_DIR"


# ---------------------------------------------------------
# INFORMACIÓN DE LA APP
# ---------------------------------------------------------

APP_NAME="VideoClipDesktop"

DISPLAY_NAME="VideoClip Desktop"

VERSION="1.0.0"

ARCH="x86_64"


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

DIST_DIR="$PROJECT_DIR/dist/$APP_NAME"

APPDIR="$PROJECT_DIR/build/AppDir"

APP_INSTALL_DIR="$APPDIR/usr/lib/videoclip-desktop"

BIN_DIR="$APPDIR/usr/bin"

APPLICATIONS_DIR="$APPDIR/usr/share/applications"

ICON_DIR="$APPDIR/usr/share/icons/hicolor/512x512/apps"

ICON_SOURCE="$PROJECT_DIR/assets/icons/videoclip-desktop.png"

APPIMAGETOOL="$PROJECT_DIR/tools/appimagetool-x86_64.AppImage"

RELEASE_DIR="$PROJECT_DIR/release"

OUTPUT_FILE="$RELEASE_DIR/VideoClip-Desktop-${VERSION}-${ARCH}.AppImage"


echo
echo "========================================"
echo " VideoClip Desktop - AppImage"
echo "========================================"
echo


# =========================================================
# VALIDACIONES
# =========================================================


if [ ! -d "$DIST_DIR" ]; then

    echo "ERROR:"
    echo "No existe el build PyInstaller:"
    echo "$DIST_DIR"

    echo
    echo "Ejecuta primero:"
    echo "./scripts/build-linux.sh"

    exit 1

fi


if [ ! -x "$DIST_DIR/$APP_NAME" ]; then

    echo "ERROR:"
    echo "No se encontró el ejecutable:"
    echo "$DIST_DIR/$APP_NAME"

    exit 1

fi


if [ ! -f "$ICON_SOURCE" ]; then

    echo "ERROR:"
    echo "No se encontró el icono:"
    echo "$ICON_SOURCE"

    exit 1

fi


if [ ! -x "$APPIMAGETOOL" ]; then

    echo "ERROR:"
    echo "No se encontró appimagetool:"
    echo "$APPIMAGETOOL"

    exit 1

fi


# =========================================================
# LIMPIAR APPDIR
# =========================================================


echo "Preparando AppDir..."

rm -rf "$APPDIR"

mkdir -p \
    "$APP_INSTALL_DIR" \
    "$BIN_DIR" \
    "$APPLICATIONS_DIR" \
    "$ICON_DIR" \
    "$RELEASE_DIR"


# =========================================================
# COPIAR BUNDLE PYINSTALLER
# =========================================================


echo "Copiando aplicación..."

cp -a \
    "$DIST_DIR/." \
    "$APP_INSTALL_DIR/"


chmod +x \
    "$APP_INSTALL_DIR/$APP_NAME"


# =========================================================
# EJECUTABLE EN usr/bin
# =========================================================


ln -s \
    "../lib/videoclip-desktop/$APP_NAME" \
    "$BIN_DIR/$APP_NAME"


# =========================================================
# ICONO
# =========================================================


cp \
    "$ICON_SOURCE" \
    "$ICON_DIR/videoclip-desktop.png"


cp \
    "$ICON_SOURCE" \
    "$APPDIR/videoclip-desktop.png"


ln -s \
    "videoclip-desktop.png" \
    "$APPDIR/.DirIcon"


# =========================================================
# DESKTOP FILE
# =========================================================


cat > "$APPLICATIONS_DIR/videoclip-desktop.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$DISPLAY_NAME
Comment=Descarga videos, extrae audio y crea clips fácilmente.
Exec=$APP_NAME
Icon=videoclip-desktop
Terminal=false
StartupNotify=true
Categories=AudioVideo;Utility;
Keywords=video;clip;audio;youtube;download;yt-dlp;
X-AppImage-Version=$VERSION
EOF


# También debe existir en la raíz del AppDir.

cp \
    "$APPLICATIONS_DIR/videoclip-desktop.desktop" \
    "$APPDIR/videoclip-desktop.desktop"


# =========================================================
# APPRUN
# =========================================================


cat > "$APPDIR/AppRun" <<'EOF'
#!/usr/bin/env bash

set -e

HERE="$(
    cd "$(dirname "$(readlink -f "$0")")"
    pwd
)"

APP_DIR="$HERE/usr/lib/videoclip-desktop"

export PATH="$HERE/usr/bin:$PATH"

exec \
    "$APP_DIR/VideoClipDesktop" \
    "$@"
EOF


chmod +x \
    "$APPDIR/AppRun"


# =========================================================
# VALIDACIÓN DEL APPDIR
# =========================================================


echo
echo "AppDir preparado:"
echo "$APPDIR"

echo
echo "Contenido principal:"

ls -lah "$APPDIR"


# =========================================================
# CREAR APPIMAGE
# =========================================================


echo
echo "Generando AppImage..."
echo


rm -f "$OUTPUT_FILE"


export ARCH="$ARCH"

export VERSION="$VERSION"


if "$APPIMAGETOOL" --version >/dev/null 2>&1; then

    "$APPIMAGETOOL" \
        --no-appstream \
        "$APPDIR" \
        "$OUTPUT_FILE"

else

    echo
    echo "FUSE no disponible."
    echo "Usando modo extract-and-run..."
    echo

    "$APPIMAGETOOL" \
        --appimage-extract-and-run \
        --no-appstream \
        "$APPDIR" \
        "$OUTPUT_FILE"

fi


# =========================================================
# PERMISOS
# =========================================================


chmod +x \
    "$OUTPUT_FILE"


# =========================================================
# RESULTADO
# =========================================================


echo
echo "========================================"
echo " APPIMAGE COMPLETADO"
echo "========================================"

echo
echo "Archivo:"
echo "$OUTPUT_FILE"

echo
echo "Tamaño:"
du -h "$OUTPUT_FILE"

echo