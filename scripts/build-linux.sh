#!/usr/bin/env bash

set -euo pipefail


# =========================================================
# VIDEOCLIP DESKTOP - BUILD LINUX
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


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

ICON_PATH="$PROJECT_DIR/assets/icons/videoclip-desktop.png"

YT_DLP_PATH="$PROJECT_DIR/assets/bin/yt-dlp"

FFMPEG_PATH="$PROJECT_DIR/assets/bin/ffmpeg"

FFPROBE_PATH="$PROJECT_DIR/assets/bin/ffprobe"


echo
echo "========================================"
echo " VideoClip Desktop - Linux Build"
echo "========================================"
echo


# =========================================================
# VALIDACIONES
# =========================================================


# ---------------------------------------------------------
# ICONO
# ---------------------------------------------------------

if [ ! -f "$ICON_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró el icono:"
    echo "$ICON_PATH"

    exit 1

fi


# ---------------------------------------------------------
# YT-DLP
# ---------------------------------------------------------

if [ ! -f "$YT_DLP_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró yt-dlp:"
    echo "$YT_DLP_PATH"

    echo
    echo "Debes preparar yt-dlp antes del build."

    exit 1

fi


# ---------------------------------------------------------
# FFMPEG
# ---------------------------------------------------------

if [ ! -f "$FFMPEG_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró ffmpeg:"
    echo "$FFMPEG_PATH"

    echo
    echo "Ejecuta:"
    echo "./scripts/fetch-ffmpeg-linux.sh"

    exit 1

fi


# ---------------------------------------------------------
# FFPROBE
# ---------------------------------------------------------

if [ ! -f "$FFPROBE_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró ffprobe:"
    echo "$FFPROBE_PATH"

    echo
    echo "Ejecuta:"
    echo "./scripts/fetch-ffmpeg-linux.sh"

    exit 1

fi


# ---------------------------------------------------------
# PYINSTALLER
# ---------------------------------------------------------

if ! command -v pyinstaller >/dev/null 2>&1; then

    echo "ERROR:"
    echo "PyInstaller no está instalado."

    echo
    echo "Ejecuta:"
    echo "python -m pip install -r requirements-dev.txt"

    exit 1

fi


# =========================================================
# MOSTRAR HERRAMIENTAS
# =========================================================

echo "Herramientas encontradas:"
echo

echo "yt-dlp:"
"$YT_DLP_PATH" --version

echo

echo "FFmpeg:"
"$FFMPEG_PATH" -version | head -n 1

echo

echo "ffprobe:"
"$FFPROBE_PATH" -version | head -n 1

echo


# =========================================================
# PERMISOS
# =========================================================

chmod +x \
    "$YT_DLP_PATH" \
    "$FFMPEG_PATH" \
    "$FFPROBE_PATH"


# =========================================================
# LIMPIAR BUILD ANTERIOR
# =========================================================

echo "Limpiando compilaciones anteriores..."

rm -rf \
    "$PROJECT_DIR/build" \
    "$PROJECT_DIR/dist"


# =========================================================
# COMPILAR
# =========================================================

echo
echo "Compilando VideoClip Desktop..."
echo


pyinstaller \
    --noconfirm \
    --clean \
    --onedir \
    --contents-directory "." \
    --name "$APP_NAME" \
    --add-data "assets/icons:assets/icons" \
    --add-binary "assets/bin/yt-dlp:assets/bin" \
    --add-binary "assets/bin/ffmpeg:assets/bin" \
    --add-binary "assets/bin/ffprobe:assets/bin" \
    main.py


# =========================================================
# RUTAS DEL BUILD
# =========================================================

DIST_DIR="$PROJECT_DIR/dist/$APP_NAME"

EXECUTABLE="$DIST_DIR/$APP_NAME"

BUNDLED_BIN_DIR="$DIST_DIR/assets/bin"

BUNDLED_YT_DLP="$BUNDLED_BIN_DIR/yt-dlp"

BUNDLED_FFMPEG="$BUNDLED_BIN_DIR/ffmpeg"

BUNDLED_FFPROBE="$BUNDLED_BIN_DIR/ffprobe"


# =========================================================
# VALIDAR RESULTADO
# =========================================================

if [ ! -f "$EXECUTABLE" ]; then

    echo
    echo "ERROR:"
    echo "El ejecutable no fue generado."

    exit 1

fi


if [ ! -f "$BUNDLED_YT_DLP" ]; then

    echo
    echo "ERROR:"
    echo "yt-dlp no fue incluido en el build."

    exit 1

fi


if [ ! -f "$BUNDLED_FFMPEG" ]; then

    echo
    echo "ERROR:"
    echo "FFmpeg no fue incluido en el build."

    exit 1

fi


if [ ! -f "$BUNDLED_FFPROBE" ]; then

    echo
    echo "ERROR:"
    echo "ffprobe no fue incluido en el build."

    exit 1

fi


# =========================================================
# PERMISOS DEL BUILD
# =========================================================

chmod +x \
    "$EXECUTABLE" \
    "$BUNDLED_YT_DLP" \
    "$BUNDLED_FFMPEG" \
    "$BUNDLED_FFPROBE"


# =========================================================
# VERIFICAR BINARIOS INCLUIDOS
# =========================================================

echo
echo "Comprobando herramientas incluidas..."
echo


echo "yt-dlp incluido:"
"$BUNDLED_YT_DLP" --version

echo


echo "FFmpeg incluido:"
"$BUNDLED_FFMPEG" -version | head -n 1

echo


echo "ffprobe incluido:"
"$BUNDLED_FFPROBE" -version | head -n 1


# =========================================================
# RESULTADO
# =========================================================

echo
echo "========================================"
echo " BUILD COMPLETADO"
echo "========================================"
echo

echo "Ejecutable:"
echo "$EXECUTABLE"

echo

echo "Herramientas incluidas:"
echo "$BUNDLED_YT_DLP"
echo "$BUNDLED_FFMPEG"
echo "$BUNDLED_FFPROBE"

echo

echo "Tamaño total:"
du -sh "$DIST_DIR"

echo