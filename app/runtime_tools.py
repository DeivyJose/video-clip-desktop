import shutil
import sys

from pathlib import Path


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

APP_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

BUNDLED_BIN_DIR = (
    APP_ROOT
    / "assets"
    / "bin"
)


def get_yt_dlp_command() -> list[str]:
    """
    Decide cómo ejecutar yt-dlp.

    Prioridad:

    1. Binario incluido con VideoClip Desktop.
    2. yt-dlp instalado en el sistema.
    3. Módulo Python del entorno actual.
    """

    # -----------------------------------------------------
    # BINARIO INCLUIDO
    # -----------------------------------------------------

    bundled_yt_dlp = (
        BUNDLED_BIN_DIR
        / "yt-dlp"
    )

    if bundled_yt_dlp.is_file():

        return [
            str(bundled_yt_dlp)
        ]

    # -----------------------------------------------------
    # INSTALACIÓN DEL SISTEMA
    # -----------------------------------------------------

    system_yt_dlp = shutil.which(
        "yt-dlp"
    )

    if system_yt_dlp:

        return [
            system_yt_dlp
        ]

    # -----------------------------------------------------
    # ENTORNO PYTHON
    # -----------------------------------------------------

    return [
        sys.executable,
        "-m",
        "yt_dlp",
    ]