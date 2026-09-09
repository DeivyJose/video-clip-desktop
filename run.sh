#!/usr/bin/env bash

set -e

PROJECT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

PYTHON="$PROJECT_DIR/.venv/bin/python"
MAIN_FILE="$PROJECT_DIR/main.py"

if [ ! -x "$PYTHON" ]; then

    if command -v notify-send >/dev/null 2>&1; then

        notify-send \
            "VideoClip Desktop" \
            "No se encontró el entorno virtual .venv."

    fi

    exit 1
fi

cd "$PROJECT_DIR"

exec "$PYTHON" "$MAIN_FILE"