import sys

from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.app_info import (
    APP_AUTHOR,
    APP_NAME,
    APP_VERSION,
)

from app.main_window import MainWindow
from app.styles import DARK_THEME


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)

ICON_PATH = (
    PROJECT_ROOT
    / "assets"
    / "icons"
    / "videoclip-desktop.png"
)


def main():
    """
    Punto de entrada principal de
    VideoClip Desktop.
    """

    app = QApplication(
        sys.argv
    )

    # -----------------------------------------------------
    # INFORMACIÓN DE LA APP
    # -----------------------------------------------------

    app.setApplicationName(
        APP_NAME
    )

    app.setApplicationDisplayName(
        APP_NAME
    )

    app.setDesktopFileName(
    "videoclip-desktop"
    )

    app.setApplicationVersion(
        APP_VERSION
    )

    app.setOrganizationName(
        APP_AUTHOR
    )

    # -----------------------------------------------------
    # ESTILO
    # -----------------------------------------------------

    app.setStyleSheet(
        DARK_THEME
    )

    # -----------------------------------------------------
    # ICONO
    # -----------------------------------------------------

    if ICON_PATH.is_file():

        icon = QIcon(
            str(ICON_PATH)
        )

        app.setWindowIcon(
            icon
        )

    # -----------------------------------------------------
    # VENTANA
    # -----------------------------------------------------

    window = MainWindow()

    if ICON_PATH.is_file():

        window.setWindowIcon(
            QIcon(
                str(ICON_PATH)
            )
        )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()