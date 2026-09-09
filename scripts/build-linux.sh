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


APP_NAME="VideoClipDesktop"

ICON_PATH="$PROJECT_DIR/assets/icons/videoclip-desktop.png"

YT_DLP_PATH="$PROJECT_DIR/assets/bin/yt-dlp"


echo
echo "========================================"
echo " VideoClip Desktop - Linux Build"
echo "========================================"
echo


# ---------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------

if [ ! -f "$ICON_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró el icono:"
    echo "$ICON_PATH"

    exit 1
fi


if [ ! -f "$YT_DLP_PATH" ]; then

    echo "ERROR:"
    echo "No se encontró yt-dlp:"
    echo "$YT_DLP_PATH"

    exit 1
fi


if ! command -v pyinstaller >/dev/null 2>&1; then

    echo "ERROR:"
    echo "PyInstaller no está instalado."

    echo
    echo "Ejecuta:"
    echo "python -m pip install -r requirements-dev.txt"

    exit 1
fi


# ---------------------------------------------------------
# PERMISOS
# ---------------------------------------------------------

chmod +x "$YT_DLP_PATH"


# ---------------------------------------------------------
# LIMPIAR BUILD ANTERIOR
# ---------------------------------------------------------

echo "Limpiando compilaciones anteriores..."

rm -rf \
    "$PROJECT_DIR/build" \
    "$PROJECT_DIR/dist"


# ---------------------------------------------------------
# COMPILAR
# ---------------------------------------------------------

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
    main.py


# ---------------------------------------------------------
# PERMISOS DEL BINARIO INCLUIDO
# ---------------------------------------------------------

BUNDLED_YT_DLP="$PROJECT_DIR/dist/$APP_NAME/assets/bin/yt-dlp"

if [ -f "$BUNDLED_YT_DLP" ]; then

    chmod +x "$BUNDLED_YT_DLP"

fi


# ---------------------------------------------------------
# RESULTADO
# ---------------------------------------------------------

EXECUTABLE="$PROJECT_DIR/dist/$APP_NAME/$APP_NAME"


echo
echo "========================================"
echo " BUILD COMPLETADO"
echo "========================================"
echo

echo "Ejecutable:"
echo "$EXECUTABLE"

echo
echo "Tamaño del paquete:"
du -sh "$PROJECT_DIR/dist/$APP_NAME"

echo