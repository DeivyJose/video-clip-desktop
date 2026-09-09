import shutil
import sys

from pathlib import Path


# =========================================================
# RUTAS DE EJECUCIÓN
# =========================================================

def get_app_root() -> Path:
    """
    Devuelve la raíz real de VideoClip Desktop.

    Funciona tanto:

    - ejecutando desde Python
    - dentro de PyInstaller
    - dentro del AppImage
    """

    if getattr(
        sys,
        "frozen",
        False
    ):

        return Path(
            sys._MEIPASS
        )

    return (
        Path(__file__)
        .resolve()
        .parents[1]
    )


APP_ROOT = get_app_root()

BUNDLED_BIN_DIR = (
    APP_ROOT
    / "assets"
    / "bin"
)


# =========================================================
# YT-DLP
# =========================================================

def get_yt_dlp_command() -> list[str]:
    """
    Decide cómo ejecutar yt-dlp.
    """

    bundled = (
        BUNDLED_BIN_DIR
        / "yt-dlp"
    )

    if bundled.is_file():

        return [
            str(bundled)
        ]

    system_yt_dlp = shutil.which(
        "yt-dlp"
    )

    if system_yt_dlp:

        return [
            system_yt_dlp
        ]

    # En desarrollo todavía podemos usar
    # el módulo Python.
    if not getattr(
        sys,
        "frozen",
        False
    ):

        return [
            sys.executable,
            "-m",
            "yt_dlp",
        ]

    raise RuntimeError(
        "No se encontró yt-dlp."
    )


# =========================================================
# FFMPEG
# =========================================================

def get_ffmpeg_path() -> str | None:
    """
    Devuelve ffmpeg incluido o el instalado
    en el sistema.
    """

    bundled = (
        BUNDLED_BIN_DIR
        / "ffmpeg"
    )

    if bundled.is_file():

        return str(
            bundled
        )

    return shutil.which(
        "ffmpeg"
    )


def get_ffprobe_path() -> str | None:
    """
    Devuelve ffprobe incluido o el instalado
    en el sistema.
    """

    bundled = (
        BUNDLED_BIN_DIR
        / "ffprobe"
    )

    if bundled.is_file():

        return str(
            bundled
        )

    return shutil.which(
        "ffprobe"
    )


def get_bundled_ffmpeg_location() -> str | None:
    """
    Si ffmpeg y ffprobe están incluidos con
    VideoClip Desktop, devuelve su directorio.

    yt-dlp recibirá este directorio mediante
    --ffmpeg-location.
    """

    ffmpeg = (
        BUNDLED_BIN_DIR
        / "ffmpeg"
    )

    ffprobe = (
        BUNDLED_BIN_DIR
        / "ffprobe"
    )

    if (
        ffmpeg.is_file()
        and
        ffprobe.is_file()
    ):

        return str(
            BUNDLED_BIN_DIR
        )

    return None