import os
import signal
import subprocess

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from app.downloader import (
    DownloadRequest,
    PROGRESS_PATTERN,
    build_download_command,
    get_video_info,
)


class AnalyzeVideoWorker(QThread):
    """
    Analiza un video en segundo plano para evitar
    que la interfaz se congele.
    """

    success = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        url: str,
        use_brave_cookies: bool = False,
        parent=None
    ):
        super().__init__(parent)

        self.url = url
        self.use_brave_cookies = use_brave_cookies

    def run(self):
        try:
            video_info = get_video_info(
                self.url,
                use_brave_cookies=self.use_brave_cookies
            )

            self.success.emit(
                video_info
            )

        except Exception as error:
            self.error.emit(
                str(error)
            )


class DownloadWorker(QThread):
    """
    Ejecuta yt-dlp en segundo plano.

    Envía a la interfaz:
    - porcentaje aproximado
    - líneas del registro
    - resultado exitoso
    - errores
    - cancelación
    """

    progress = Signal(int)
    log = Signal(str)

    success = Signal(str)
    error = Signal(str)

    canceled = Signal()

    def __init__(
        self,
        request: DownloadRequest,
        parent=None
    ):
        super().__init__(parent)

        self.request = request

        self.process = None

        self.cancel_requested = False

        self.last_progress = 0

    def run(self):
        try:
            destination = (
                Path(self.request.destination)
                .expanduser()
                .resolve()
            )

            destination.mkdir(
                parents=True,
                exist_ok=True
            )

            command = build_download_command(
                self.request
            )

            self.log.emit(
                "Iniciando yt-dlp..."
            )

            self.log.emit(
                f"Destino: {destination}"
            )

            self.process = subprocess.Popen(
                command,

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                bufsize=1,

                # Permite terminar también los procesos hijos,
                # como FFmpeg.
                start_new_session=True
            )

            if self.process.stdout is None:
                raise RuntimeError(
                    "No se pudo leer la salida de yt-dlp."
                )

            for raw_line in self.process.stdout:

                if self.cancel_requested:
                    break

                line = raw_line.rstrip()

                if not line:
                    continue

                self.log.emit(
                    line
                )

                match = PROGRESS_PATTERN.search(
                    line
                )

                if match:

                    percentage = int(
                        float(
                            match.group(1)
                        )
                    )

                    # Reservamos el 100 % real para cuando
                    # yt-dlp + FFmpeg hayan terminado totalmente.
                    percentage = min(
                        percentage,
                        95
                    )

                    # Evita que la barra retroceda cuando
                    # yt-dlp descarga video y audio por separado.
                    if percentage > self.last_progress:

                        self.last_progress = percentage

                        self.progress.emit(
                            percentage
                        )

            if self.cancel_requested:

                self.stop_process()

                self.canceled.emit()

                return

            return_code = (
                self.process.wait()
            )

            if return_code != 0:

                raise RuntimeError(
                    "yt-dlp terminó con un error. "
                    "Revisa el registro para más detalles."
                )

            self.progress.emit(
                100
            )

            self.success.emit(
                str(destination)
            )

        except Exception as error:

            if self.cancel_requested:

                self.canceled.emit()

            else:

                self.error.emit(
                    str(error)
                )

    def cancel(self):
        """
        Solicita cancelar la descarga actual.
        """

        self.cancel_requested = True

        self.stop_process()

    def stop_process(self):
        """
        Detiene yt-dlp y también su proceso hijo FFmpeg.
        """

        if self.process is None:
            return

        if self.process.poll() is not None:
            return

        try:

            process_group = os.getpgid(
                self.process.pid
            )

            os.killpg(
                process_group,
                signal.SIGTERM
            )

        except (ProcessLookupError, OSError):

            try:
                self.process.terminate()

            except OSError:
                pass