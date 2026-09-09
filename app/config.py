import json
import os
from pathlib import Path


# Nombre interno que utilizaremos para la configuración.
APP_NAME = "video-clip-desktop"


# En Linux normalmente las aplicaciones guardan su configuración
# dentro de ~/.config/
CONFIG_DIR = Path(
    os.environ.get(
        "XDG_CONFIG_HOME",
        Path.home() / ".config"
    )
) / APP_NAME


# Archivo donde guardaremos las preferencias.
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_default_download_folder() -> Path:
    """
    Devuelve una carpeta razonable para utilizar como destino
    inicial de las descargas.
    """

    possible_folders = [
        Path.home() / "Descargas",
        Path.home() / "Downloads",
    ]

    for folder in possible_folders:
        if folder.exists():
            return folder

    # Si ninguna existe, utilizamos el directorio personal.
    return Path.home()


class AppConfig:
    """
    Se encarga de cargar y guardar las preferencias
    de VideoClip Desktop.
    """

    def __init__(self):

        default_folder = str(
            get_default_download_folder()
        )

        # Estos son los valores que tendrá la aplicación
        # cuando se ejecute por primera vez.
        self.data = {
            "favorite_folders": [
                default_folder
            ],
            "last_folder": default_folder,
            "use_brave_cookies": False,
        }

        self.load()

    @property
    def favorite_folders(self) -> list[str]:
        """
        Devuelve las carpetas favoritas guardadas.
        """

        return self.data.get(
            "favorite_folders",
            []
        )

    @property
    def last_folder(self) -> str:
        """
        Devuelve la última carpeta utilizada.
        """

        return self.data.get(
            "last_folder",
            str(get_default_download_folder())
        )

    @last_folder.setter
    def last_folder(self, value: str):
        """
        Cambia y guarda la última carpeta utilizada.
        """

        self.data["last_folder"] = value
        self.save()

    @property
    def use_brave_cookies(self) -> bool:
        return bool(
            self.data.get(
                "use_brave_cookies",
                False
            )
        )

    @use_brave_cookies.setter
    def use_brave_cookies(self, value: bool):
        self.data["use_brave_cookies"] = bool(
            value
        )

        self.save()

    def load(self):
        """
        Carga config.json si ya existe.
        """

        if not CONFIG_FILE.exists():

            # Primera ejecución.
            self.save()
            return

        try:

            content = CONFIG_FILE.read_text(
                encoding="utf-8"
            )

            saved_data = json.loads(
                content
            )

            if isinstance(saved_data, dict):
                self.data.update(
                    saved_data
                )

        except (
            json.JSONDecodeError,
            OSError
        ):
            # Si el archivo está dañado,
            # conservamos los valores por defecto.
            pass

        self.clean_favorites()

    def save(self):
        """
        Guarda las preferencias en config.json.
        """

        CONFIG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        CONFIG_FILE.write_text(
            json.dumps(
                self.data,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def add_favorite_folder(
        self,
        folder: str
    ):
        """
        Agrega una carpeta a favoritos.
        """

        folder_path = (
            Path(folder)
            .expanduser()
            .resolve()
        )

        folder_string = str(
            folder_path
        )

        favorites = (
            self.favorite_folders.copy()
        )

        if folder_string not in favorites:

            favorites.append(
                folder_string
            )

            self.data[
                "favorite_folders"
            ] = favorites

            self.save()

    def remove_favorite_folder(
        self,
        folder: str
    ):
        """
        Elimina una carpeta de favoritos.
        """

        favorites = [
            item
            for item in self.favorite_folders
            if item != folder
        ]

        # Siempre queremos tener por lo menos
        # una ruta disponible.
        if not favorites:

            favorites = [
                str(
                    get_default_download_folder()
                )
            ]

        self.data[
            "favorite_folders"
        ] = favorites

        self.save()

    def clean_favorites(self):
        """
        Elimina rutas duplicadas o vacías.
        """

        clean_list = []

        for folder in self.favorite_folders:

            if not folder:
                continue

            normalized = str(
                Path(folder).expanduser()
            )

            if normalized not in clean_list:

                clean_list.append(
                    normalized
                )

        if not clean_list:

            clean_list = [
                str(
                    get_default_download_folder()
                )
            ]

        self.data[
            "favorite_folders"
        ] = clean_list

        if not self.data.get(
            "last_folder"
        ):

            self.data[
                "last_folder"
            ] = clean_list[0]

        self.save()