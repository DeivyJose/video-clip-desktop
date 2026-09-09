#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

RUN_SCRIPT="$PROJECT_DIR/run.sh"

ICON_PATH="$PROJECT_DIR/assets/icons/videoclip-desktop.png"

APPLICATIONS_DIR="$HOME/.local/share/applications"

DESKTOP_FILE="$APPLICATIONS_DIR/videoclip-desktop.desktop"


echo
echo "Instalando VideoClip Desktop..."
echo


# ---------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------

if [ ! -f "$RUN_SCRIPT" ]; then
    echo "ERROR: No se encontró run.sh"
    exit 1
fi


if [ ! -f "$ICON_PATH" ]; then
    echo "ERROR: No se encontró el icono:"
    echo "$ICON_PATH"
    exit 1
fi


# ---------------------------------------------------------
# DIRECTORIO DE APLICACIONES
# ---------------------------------------------------------

mkdir -p "$APPLICATIONS_DIR"


# ---------------------------------------------------------
# CREAR .DESKTOP
# ---------------------------------------------------------

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application

Name=VideoClip Desktop

Comment=Descarga videos, extrae audio y crea clips fácilmente.

Exec=$RUN_SCRIPT

Icon=$ICON_PATH

Path=$PROJECT_DIR

Terminal=false

StartupNotify=true

Categories=AudioVideo;Utility;

Keywords=video;clip;audio;youtube;download;yt-dlp;

EOF


# ---------------------------------------------------------
# PERMISOS
# ---------------------------------------------------------

chmod +x "$DESKTOP_FILE"


# ---------------------------------------------------------
# VALIDAR
# ---------------------------------------------------------

if command -v desktop-file-validate >/dev/null 2>&1; then

    desktop-file-validate \
        "$DESKTOP_FILE"

fi


# ---------------------------------------------------------
# ACTUALIZAR BASE DE DATOS
# ---------------------------------------------------------

if command -v update-desktop-database >/dev/null 2>&1; then

    update-desktop-database \
        "$APPLICATIONS_DIR"

fi


echo
echo "VideoClip Desktop instalado correctamente."
echo
echo "Launcher:"
echo "$DESKTOP_FILE"
echo
echo "Ahora busca 'VideoClip Desktop' en el menú de aplicaciones."
echo