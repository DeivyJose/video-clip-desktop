#!/usr/bin/env bash

set -euo pipefail


# =========================================================
# VIDEOCLIP DESKTOP - DESCARGAR FFMPEG PARA LINUX
# =========================================================


PROJECT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

cd "$PROJECT_DIR"


BIN_DIR="$PROJECT_DIR/assets/bin"

TEMP_DIR="$(
    mktemp -d
)"

ARCHIVE_NAME="ffmpeg-n9.0-latest-linux64-lgpl-9.0.tar.xz"


cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT


echo
echo "========================================"
echo " VideoClip Desktop - FFmpeg"
echo "========================================"
echo


# ---------------------------------------------------------
# COMPROBAR GITHUB CLI
# ---------------------------------------------------------

if ! command -v gh >/dev/null 2>&1; then

    echo "ERROR:"
    echo "GitHub CLI (gh) no está instalado."

    exit 1
fi


# ---------------------------------------------------------
# PREPARAR DIRECTORIO
# ---------------------------------------------------------

mkdir -p "$BIN_DIR"

mkdir -p "$TEMP_DIR/extracted"


# ---------------------------------------------------------
# DESCARGAR
# ---------------------------------------------------------

echo "Descargando FFmpeg Linux x86_64 LGPL..."
echo

gh release download \
    --repo BtbN/FFmpeg-Builds \
    --pattern "$ARCHIVE_NAME" \
    --dir "$TEMP_DIR" \
    --clobber


ARCHIVE="$TEMP_DIR/$ARCHIVE_NAME"


if [ ! -f "$ARCHIVE" ]; then

    echo
    echo "ERROR:"
    echo "No se pudo descargar FFmpeg."

    exit 1
fi


# ---------------------------------------------------------
# EXTRAER
# ---------------------------------------------------------

echo
echo "Extrayendo..."
echo

tar -xf \
    "$ARCHIVE" \
    -C "$TEMP_DIR/extracted"


# ---------------------------------------------------------
# LOCALIZAR BINARIOS
# ---------------------------------------------------------

FFMPEG_SOURCE="$(
    find "$TEMP_DIR/extracted" \
        -type f \
        -path "*/bin/ffmpeg" \
        -print \
        -quit
)"

FFPROBE_SOURCE="$(
    find "$TEMP_DIR/extracted" \
        -type f \
        -path "*/bin/ffprobe" \
        -print \
        -quit
)"


if [ -z "$FFMPEG_SOURCE" ]; then

    echo "ERROR:"
    echo "No se encontró el binario ffmpeg."

    exit 1
fi


if [ -z "$FFPROBE_SOURCE" ]; then

    echo "ERROR:"
    echo "No se encontró el binario ffprobe."

    exit 1
fi


# ---------------------------------------------------------
# COPIAR
# ---------------------------------------------------------

echo "Copiando ffmpeg..."

cp \
    "$FFMPEG_SOURCE" \
    "$BIN_DIR/ffmpeg"


echo "Copiando ffprobe..."

cp \
    "$FFPROBE_SOURCE" \
    "$BIN_DIR/ffprobe"


chmod +x \
    "$BIN_DIR/ffmpeg" \
    "$BIN_DIR/ffprobe"


# ---------------------------------------------------------
# COMPROBAR
# ---------------------------------------------------------

echo
echo "FFmpeg:"
"$BIN_DIR/ffmpeg" -version | head -n 1

echo
echo "ffprobe:"
"$BIN_DIR/ffprobe" -version | head -n 1


echo
echo "========================================"
echo " FFMPEG PREPARADO"
echo "========================================"

echo
echo "Archivos:"
echo "$BIN_DIR/ffmpeg"
echo "$BIN_DIR/ffprobe"
echo