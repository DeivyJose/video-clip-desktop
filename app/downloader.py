import argparse
import json
import re
import shutil
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


# ---------------------------------------------------------
# Constantes
# ---------------------------------------------------------

MODE_VIDEO = "video"
MODE_CLIP = "clip"
MODE_AUDIO = "audio"


PROGRESS_PATTERN = re.compile(
    r"\[download\]\s+(\d+(?:\.\d+)?)%"
)


# ---------------------------------------------------------
# Modelos de datos
# ---------------------------------------------------------

@dataclass
class VideoInfo:
    """
    Información básica obtenida de un video.
    """

    title: str
    channel: str
    duration: int
    duration_text: str
    webpage_url: str
    thumbnail: str | None = None


@dataclass
class DownloadRequest:
    """
    Representa todo lo necesario para realizar
    una descarga.
    """

    url: str
    destination: str

    mode: str = MODE_VIDEO
    quality: str = "best"

    start_time: str = ""
    end_time: str = ""

    precise_cut: bool = True
    use_brave_cookies: bool = False


# ---------------------------------------------------------
# Validaciones
# ---------------------------------------------------------

def check_dependencies():
    """
    Comprueba que FFmpeg exista en el sistema.
    """

    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "FFmpeg no está instalado o no se encuentra "
            "en el PATH del sistema."
        )

    if shutil.which("ffprobe") is None:
        raise RuntimeError(
            "ffprobe no está instalado. Normalmente viene "
            "incluido junto con FFmpeg."
        )


def validate_url(url: str):
    """
    Comprueba que el texto tenga forma de URL HTTP/HTTPS.

    No nos limitamos estrictamente a youtube.com porque
    yt-dlp puede funcionar con muchos sitios y esto nos
    deja abierta esa posibilidad para el futuro.
    """

    parsed = urlparse(
        url.strip()
    )

    if parsed.scheme not in {
        "http",
        "https"
    }:
        raise ValueError(
            "La URL debe comenzar con http:// o https://"
        )

    if not parsed.netloc:
        raise ValueError(
            "La URL no parece válida."
        )


# ---------------------------------------------------------
# Manejo de tiempos
# ---------------------------------------------------------

def time_to_seconds(value: str) -> int:
    """
    Convierte distintos formatos de tiempo a segundos.

    Ejemplos:

    30
    01:30
    00:01:30

    Todos representan cantidades de tiempo.
    """

    value = value.strip()

    if not value:
        raise ValueError(
            "El tiempo no puede estar vacío."
        )

    parts = value.split(":")

    if len(parts) > 3:
        raise ValueError(
            "Formato de tiempo inválido."
        )

    try:
        numbers = [
            int(part)
            for part in parts
        ]

    except ValueError as error:

        raise ValueError(
            "El tiempo solo puede contener números "
            "separados por ':'."
        ) from error

    if any(
        number < 0
        for number in numbers
    ):
        raise ValueError(
            "El tiempo no puede ser negativo."
        )

    # Ejemplo:
    # 30
    if len(numbers) == 1:
        return numbers[0]

    # Ejemplo:
    # 01:30
    if len(numbers) == 2:

        minutes, seconds = numbers

        if seconds >= 60:
            raise ValueError(
                "Los segundos deben ser menores de 60."
            )

        return (
            minutes * 60
            + seconds
        )

    # Ejemplo:
    # 01:05:30
    hours, minutes, seconds = numbers

    if minutes >= 60:
        raise ValueError(
            "Los minutos deben ser menores de 60."
        )

    if seconds >= 60:
        raise ValueError(
            "Los segundos deben ser menores de 60."
        )

    return (
        hours * 3600
        + minutes * 60
        + seconds
    )


def seconds_to_timestamp(
    total_seconds: int
) -> str:
    """
    Convierte segundos a HH:MM:SS.
    """

    hours, remainder = divmod(
        total_seconds,
        3600
    )

    minutes, seconds = divmod(
        remainder,
        60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


def filename_timestamp(
    value: str
) -> str:
    """
    Convierte:

    00:01:25

    en:

    00-01-25

    para utilizarlo cómodamente dentro del nombre
    de un archivo.
    """

    seconds = time_to_seconds(
        value
    )

    timestamp = seconds_to_timestamp(
        seconds
    )

    return timestamp.replace(
        ":",
        "-"
    )


# ---------------------------------------------------------
# Calidad de video
# ---------------------------------------------------------

def get_format_selector(
    quality: str
) -> str:
    """
    Devuelve el selector de formatos que utilizará yt-dlp.
    """

    formats = {
        "best": (
            "bv*[ext=mp4]+ba[ext=m4a]/"
            "b[ext=mp4]/"
            "bv*+ba/b"
        ),

        "1080p": (
            "bv*[height<=1080][ext=mp4]"
            "+ba[ext=m4a]/"
            "b[height<=1080][ext=mp4]/"
            "bv*[height<=1080]+ba/"
            "b[height<=1080]"
        ),

        "720p": (
            "bv*[height<=720][ext=mp4]"
            "+ba[ext=m4a]/"
            "b[height<=720][ext=mp4]/"
            "bv*[height<=720]+ba/"
            "b[height<=720]"
        ),

        "480p": (
            "bv*[height<=480][ext=mp4]"
            "+ba[ext=m4a]/"
            "b[height<=480][ext=mp4]/"
            "bv*[height<=480]+ba/"
            "b[height<=480]"
        ),
    }

    if quality not in formats:
        raise ValueError(
            f"Calidad no reconocida: {quality}"
        )

    return formats[quality]


# ---------------------------------------------------------
# Cookies de Brave
# ---------------------------------------------------------

def add_browser_cookies(
    command: list[str],
    use_brave_cookies: bool
):
    """
    Si el usuario lo solicita, yt-dlp intentará utilizar
    la sesión existente de Brave.
    """

    if use_brave_cookies:

        command.extend([
            "--cookies-from-browser",
            "brave"
        ])


# ---------------------------------------------------------
# Analizar un video
# ---------------------------------------------------------

def get_video_info(
    url: str,
    use_brave_cookies: bool = False
) -> VideoInfo:
    """
    Obtiene información del video sin descargarlo.
    """

    validate_url(
        url
    )

    command = [
        sys.executable,
        "-m",
        "yt_dlp",

        "--dump-single-json",
        "--skip-download",
        "--no-playlist",
    ]

    add_browser_cookies(
        command,
        use_brave_cookies
    )

    command.append(
        url
    )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:

        error_message = (
            result.stderr.strip()
            or
            "No se pudo analizar el video."
        )

        raise RuntimeError(
            error_message
        )

    try:

        data = json.loads(
            result.stdout
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            "yt-dlp respondió, pero no devolvió "
            "información JSON válida."
        ) from error

    duration = int(
        data.get("duration")
        or 0
    )

    return VideoInfo(
        title=(
            data.get("title")
            or "Sin título"
        ),

        channel=(
            data.get("channel")
            or
            data.get("uploader")
            or
            "Desconocido"
        ),

        duration=duration,

        duration_text=(
            data.get("duration_string")
            or seconds_to_timestamp(
                duration
            )
        ),

        webpage_url=(
            data.get("webpage_url")
            or url
        ),

        thumbnail=data.get(
            "thumbnail"
        ),
    )


# ---------------------------------------------------------
# Crear el comando de yt-dlp
# ---------------------------------------------------------

def build_download_command(
    request: DownloadRequest
) -> list[str]:
    """
    Construye el comando que ejecutará yt-dlp.

    Importante:
    esta función todavía NO descarga nada.
    Solo prepara las instrucciones.
    """

    validate_url(
        request.url
    )

    destination = str(
        Path(
            request.destination
        )
        .expanduser()
        .resolve()
    )

    command = [
        sys.executable,
        "-m",
        "yt_dlp",

        # Hace que el progreso aparezca
        # línea por línea.
        "--newline",

        # Por ahora no permitiremos playlists.
        "--no-playlist",

        # Evita sobrescribir accidentalmente
        # un archivo existente.
        "--no-overwrites",

        # Carpeta final.
        "-P",
        destination,
    ]

    add_browser_cookies(
        command,
        request.use_brave_cookies
    )

    # -----------------------------------------------------
    # MODO AUDIO
    # -----------------------------------------------------

    if request.mode == MODE_AUDIO:

        output_template = (
            "%(title)s [%(id)s].%(ext)s"
        )

        command.extend([
            "-o",
            output_template,

            "-x",

            "--audio-format",
            "mp3",

            "--audio-quality",
            "0",
        ])

    # -----------------------------------------------------
    # VIDEO COMPLETO O CLIP
    # -----------------------------------------------------

    elif request.mode in {
        MODE_VIDEO,
        MODE_CLIP
    }:

        format_selector = (
            get_format_selector(
                request.quality
            )
        )

        command.extend([
            "-f",
            format_selector,

            "--merge-output-format",
            "mp4",
        ])

        # ---------------------------------------------
        # VIDEO COMPLETO
        # ---------------------------------------------

        if request.mode == MODE_VIDEO:

            command.extend([
                "-o",
                (
                    "%(title)s "
                    "[%(id)s].%(ext)s"
                ),
            ])

        # ---------------------------------------------
        # RECORTE
        # ---------------------------------------------

        else:

            start_seconds = (
                time_to_seconds(
                    request.start_time
                )
            )

            end_seconds = (
                time_to_seconds(
                    request.end_time
                )
            )

            if end_seconds <= start_seconds:

                raise ValueError(
                    "El tiempo final debe ser mayor "
                    "que el tiempo inicial."
                )

            start_timestamp = (
                seconds_to_timestamp(
                    start_seconds
                )
            )

            end_timestamp = (
                seconds_to_timestamp(
                    end_seconds
                )
            )

            section = (
                f"*"
                f"{start_timestamp}"
                f"-"
                f"{end_timestamp}"
            )

            start_filename = (
                filename_timestamp(
                    request.start_time
                )
            )

            end_filename = (
                filename_timestamp(
                    request.end_time
                )
            )

            output_template = (
                "%(title)s "
                "[%(id)s] "
                f"[clip {start_filename}"
                f"_to_{end_filename}]"
                ".%(ext)s"
            )

            command.extend([
                "-o",
                output_template,

                "--download-sections",
                section,
            ])

            if request.precise_cut:

                command.append(
                    "--force-keyframes-at-cuts"
                )

    else:

        raise ValueError(
            f"Modo desconocido: {request.mode}"
        )

    command.append(
        request.url
    )

    return command


# ---------------------------------------------------------
# Ejecutar la descarga
# ---------------------------------------------------------

def download(
    request: DownloadRequest
):
    """
    Ejecuta la descarga y muestra el progreso
    en la terminal.

    Más adelante la interfaz gráfica escuchará
    este mismo proceso.
    """

    check_dependencies()

    destination = (
        Path(
            request.destination
        )
        .expanduser()
        .resolve()
    )

    destination.mkdir(
        parents=True,
        exist_ok=True
    )

    command = build_download_command(
        request
    )

    print()
    print(
        "Iniciando yt-dlp..."
    )
    print(
        f"Destino: {destination}"
    )
    print()

    process = subprocess.Popen(
        command,

        stdout=subprocess.PIPE,

        stderr=subprocess.STDOUT,

        text=True,

        bufsize=1
    )

    if process.stdout is None:

        raise RuntimeError(
            "No se pudo leer la salida de yt-dlp."
        )

    for line in process.stdout:

        line = line.rstrip()

        if not line:
            continue

        print(
            line
        )

        # Más adelante utilizaremos este porcentaje
        # para alimentar la barra de progreso.
        match = PROGRESS_PATTERN.search(
            line
        )

        if match:

            percentage = float(
                match.group(1)
            )

            # Por ahora simplemente tenemos disponible
            # la variable percentage.
            # La GUI la utilizará después.
            _ = percentage

    return_code = process.wait()

    if return_code != 0:

        raise RuntimeError(
            "yt-dlp terminó con un error."
        )

    print()
    print(
        "Proceso completado correctamente."
    )
    print(
        f"Archivos guardados en: {destination}"
    )


# ---------------------------------------------------------
# Interfaz temporal para probar desde terminal
# ---------------------------------------------------------

def create_parser():
    """
    Crea los comandos de prueba.

    Esto desaparecerá o quedará como herramienta
    secundaria cuando tengamos la GUI.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Motor de descargas de "
            "VideoClip Desktop"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # -----------------------------------------------------
    # ANALIZAR
    # -----------------------------------------------------

    analyze_parser = (
        subparsers.add_parser(
            "analyze",
            help="Analizar un video sin descargarlo"
        )
    )

    analyze_parser.add_argument(
        "url"
    )

    analyze_parser.add_argument(
        "--brave",
        action="store_true",
        help="Utilizar cookies de Brave"
    )

    # -----------------------------------------------------
    # DESCARGAR VIDEO COMPLETO
    # -----------------------------------------------------

    video_parser = (
        subparsers.add_parser(
            "video",
            help="Descargar video completo"
        )
    )

    video_parser.add_argument(
        "url"
    )

    video_parser.add_argument(
        "-o",
        "--output",
        required=True
    )

    video_parser.add_argument(
        "-q",
        "--quality",
        choices=[
            "best",
            "1080p",
            "720p",
            "480p"
        ],
        default="best"
    )

    video_parser.add_argument(
        "--brave",
        action="store_true"
    )

    # -----------------------------------------------------
    # RECORTE
    # -----------------------------------------------------

    clip_parser = (
        subparsers.add_parser(
            "clip",
            help="Descargar solamente una sección"
        )
    )

    clip_parser.add_argument(
        "url"
    )

    clip_parser.add_argument(
        "--start",
        required=True,
        help="Ejemplo: 00:01:10"
    )

    clip_parser.add_argument(
        "--end",
        required=True,
        help="Ejemplo: 00:01:40"
    )

    clip_parser.add_argument(
        "-o",
        "--output",
        required=True
    )

    clip_parser.add_argument(
        "-q",
        "--quality",
        choices=[
            "best",
            "1080p",
            "720p",
            "480p"
        ],
        default="best"
    )

    clip_parser.add_argument(
        "--fast-cut",
        action="store_true",
        help=(
            "No forzar keyframes. "
            "Es más rápido, pero menos preciso."
        )
    )

    clip_parser.add_argument(
        "--brave",
        action="store_true"
    )

    # -----------------------------------------------------
    # AUDIO
    # -----------------------------------------------------

    audio_parser = (
        subparsers.add_parser(
            "audio",
            help="Extraer el audio como MP3"
        )
    )

    audio_parser.add_argument(
        "url"
    )

    audio_parser.add_argument(
        "-o",
        "--output",
        required=True
    )

    audio_parser.add_argument(
        "--brave",
        action="store_true"
    )

    return parser


def main():
    """
    Entrada temporal por terminal.
    """

    parser = create_parser()

    args = parser.parse_args()

    try:

        # -------------------------------------------------
        # ANALIZAR
        # -------------------------------------------------

        if args.command == "analyze":

            info = get_video_info(
                args.url,
                use_brave_cookies=args.brave
            )

            print()
            print(
                f"Título:   {info.title}"
            )

            print(
                f"Canal:    {info.channel}"
            )

            print(
                f"Duración: {info.duration_text}"
            )

            print(
                f"URL:      {info.webpage_url}"
            )

            return

        # -------------------------------------------------
        # VIDEO COMPLETO
        # -------------------------------------------------

        if args.command == "video":

            request = DownloadRequest(
                url=args.url,
                destination=args.output,
                mode=MODE_VIDEO,
                quality=args.quality,
                use_brave_cookies=args.brave
            )

        # -------------------------------------------------
        # CLIP
        # -------------------------------------------------

        elif args.command == "clip":

            request = DownloadRequest(
                url=args.url,
                destination=args.output,
                mode=MODE_CLIP,
                quality=args.quality,
                start_time=args.start,
                end_time=args.end,
                precise_cut=not args.fast_cut,
                use_brave_cookies=args.brave
            )

        # -------------------------------------------------
        # AUDIO
        # -------------------------------------------------

        else:

            request = DownloadRequest(
                url=args.url,
                destination=args.output,
                mode=MODE_AUDIO,
                use_brave_cookies=args.brave
            )

        download(
            request
        )

    except (
        ValueError,
        RuntimeError
    ) as error:

        print()
        print(
            f"ERROR: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()