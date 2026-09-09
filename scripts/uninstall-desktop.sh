#!/usr/bin/env bash

set -e

DESKTOP_FILE="$HOME/.local/share/applications/videoclip-desktop.desktop"

if [ -f "$DESKTOP_FILE" ]; then

    rm "$DESKTOP_FILE"

    echo
    echo "Launcher de VideoClip Desktop eliminado."
    echo

else

    echo
    echo "VideoClip Desktop no estaba instalado en el menú."
    echo

fi


if command -v update-desktop-database >/dev/null 2>&1; then

    update-desktop-database \
        "$HOME/.local/share/applications"

fi