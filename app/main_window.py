from pathlib import Path


from PySide6.QtCore import (
    Qt,
    QUrl,
)

from PySide6.QtGui import (
    QCloseEvent,
    QDesktopServices,
)

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


from app.config import AppConfig

from app.downloader import (
    DownloadRequest,
    MODE_AUDIO,
    MODE_CLIP,
    MODE_VIDEO,
    time_to_seconds,
)

from app.workers import (
    AnalyzeVideoWorker,
    DownloadWorker,
)


# =========================================================
# REDES SOCIALES
# =========================================================

GITHUB_URL = (
    "https://github.com/DeivyJose"
)

# Antes de publicar reemplazaremos estas dos
# por tus enlaces exactos.
LINKEDIN_URL = (
    "https://www.linkedin.com/in/deivy-jose-ure%C3%B1a-namias-6058a9237/"
)

INSTAGRAM_URL = ""


# =========================================================
# ADMINISTRADOR DE CARPETAS
# =========================================================

class FolderManagerDialog(QDialog):

    def __init__(
        self,
        config: AppConfig,
        parent=None
    ):
        super().__init__(parent)

        self.config = config

        self.setWindowTitle(
            "Administrar carpetas"
        )

        self.resize(
            650,
            380
        )

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "Carpetas favoritas"
        )

        title.setObjectName(
            "VideoTitle"
        )

        layout.addWidget(
            title
        )

        description = QLabel(
            "Estas rutas aparecerán directamente "
            "en VideoClip Desktop."
        )

        description.setObjectName(
            "SecondaryText"
        )

        layout.addWidget(
            description
        )

        self.folder_list = QListWidget()

        layout.addWidget(
            self.folder_list,
            1
        )

        buttons = QHBoxLayout()

        add_button = QPushButton(
            "Agregar"
        )

        remove_button = QPushButton(
            "Eliminar"
        )

        open_button = QPushButton(
            "Abrir"
        )

        close_button = QPushButton(
            "Cerrar"
        )

        add_button.clicked.connect(
            self.add_folder
        )

        remove_button.clicked.connect(
            self.remove_folder
        )

        open_button.clicked.connect(
            self.open_folder
        )

        close_button.clicked.connect(
            self.accept
        )

        buttons.addWidget(
            add_button
        )

        buttons.addWidget(
            remove_button
        )

        buttons.addWidget(
            open_button
        )

        buttons.addStretch()

        buttons.addWidget(
            close_button
        )

        layout.addLayout(
            buttons
        )

        self.refresh()

    def refresh(self):

        self.folder_list.clear()

        self.folder_list.addItems(
            self.config.favorite_folders
        )

    def add_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta",
            self.config.last_folder
        )

        if not folder:
            return

        self.config.add_favorite_folder(
            folder
        )

        self.config.last_folder = (
            folder
        )

        self.refresh()

    def remove_folder(self):

        item = (
            self.folder_list
            .currentItem()
        )

        if item is None:

            QMessageBox.information(
                self,
                "Selecciona una carpeta",
                "Selecciona primero la ruta "
                "que deseas eliminar."
            )

            return

        self.config.remove_favorite_folder(
            item.text()
        )

        self.refresh()

    def open_folder(self):

        item = (
            self.folder_list
            .currentItem()
        )

        if item is None:
            return

        path = (
            Path(item.text())
            .expanduser()
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "La carpeta no existe",
                "Esta ruta ya no existe en el sistema."
            )

            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(path.resolve())
            )
        )


# =========================================================
# VENTANA PRINCIPAL
# =========================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.config = AppConfig()

        self.analyze_worker = None

        self.download_worker = None

        self.current_video_info = None

        self.setWindowTitle(
            "VideoClip Desktop"
        )

        self.resize(
            980,
            850
        )

        self.setMinimumSize(
            820,
            650
        )

        self.build_interface()

    # =====================================================
    # INTERFAZ GENERAL
    # =====================================================

    def build_interface(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        root_layout = QVBoxLayout(
            central_widget
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            8
        )

        root_layout.setSpacing(
            0
        )

        # -------------------------------------------------
        # SCROLL PRINCIPAL
        # -------------------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        content = QWidget()

        self.main_layout = QVBoxLayout(
            content
        )

        self.main_layout.setContentsMargins(
            28,
            24,
            28,
            24
        )

        self.main_layout.setSpacing(
            18
        )

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll,
            1
        )

        # -------------------------------------------------
        # SECCIONES
        # -------------------------------------------------

        self.build_header()

        self.build_url_section()

        self.build_video_info_section()

        self.build_options_section()

        self.build_destination_section()

        self.build_download_section()

        self.main_layout.addStretch()

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------

        self.build_footer(
            root_layout
        )

    # =====================================================
    # HEADER
    # =====================================================

    def build_header(self):

        title = QLabel(
            "VideoClip Desktop"
        )

        title.setObjectName(
            "AppTitle"
        )

        subtitle = QLabel(
            "Descarga videos, extrae audio "
            "y crea clips desde una sola aplicación."
        )

        subtitle.setObjectName(
            "AppSubtitle"
        )

        self.main_layout.addWidget(
            title
        )

        self.main_layout.addWidget(
            subtitle
        )

    # =====================================================
    # TARJETAS
    # =====================================================

    def create_card(self):

        card = QFrame()

        card.setObjectName(
            "Card"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        layout.setSpacing(
            12
        )

        return card, layout

    # =====================================================
    # URL
    # =====================================================

    def build_url_section(self):

        card, layout = (
            self.create_card()
        )

        title = QLabel(
            "ENLACE DEL VIDEO"
        )

        title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            title
        )

        row = QHBoxLayout()

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Pega aquí un enlace de YouTube..."
        )

        self.url_input.returnPressed.connect(
            self.analyze_video
        )

        self.analyze_button = QPushButton(
            "Analizar"
        )

        self.analyze_button.setObjectName(
            "PrimaryButton"
        )

        self.analyze_button.clicked.connect(
            self.analyze_video
        )

        row.addWidget(
            self.url_input,
            1
        )

        row.addWidget(
            self.analyze_button
        )

        layout.addLayout(
            row
        )

        self.brave_checkbox = QCheckBox(
            "Usar mi sesión de Brave si YouTube "
            "requiere autenticación"
        )

        self.brave_checkbox.setChecked(
            self.config.use_brave_cookies
        )

        self.brave_checkbox.toggled.connect(
            self.save_brave_preference
        )

        layout.addWidget(
            self.brave_checkbox
        )

        self.main_layout.addWidget(
            card
        )

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def build_video_info_section(self):

        card, layout = (
            self.create_card()
        )

        title = QLabel(
            "INFORMACIÓN DEL VIDEO"
        )

        title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            title
        )

        self.video_title_label = QLabel(
            "Aún no se ha analizado ningún video."
        )

        self.video_title_label.setObjectName(
            "VideoTitle"
        )

        self.video_title_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.video_title_label
        )

        self.channel_label = QLabel(
            "Canal: —"
        )

        self.channel_label.setObjectName(
            "SecondaryText"
        )

        self.duration_label = QLabel(
            "Duración: —"
        )

        self.duration_label.setObjectName(
            "SecondaryText"
        )

        self.video_status_label = QLabel(
            "Pega un enlace para comenzar."
        )

        self.video_status_label.setObjectName(
            "StatusText"
        )

        layout.addWidget(
            self.channel_label
        )

        layout.addWidget(
            self.duration_label
        )

        layout.addWidget(
            self.video_status_label
        )

        self.main_layout.addWidget(
            card
        )

    # =====================================================
    # OPCIONES
    # =====================================================

    def build_options_section(self):

        card, layout = (
            self.create_card()
        )

        title = QLabel(
            "OPCIONES"
        )

        title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            title
        )

        grid = QGridLayout()

        grid.setHorizontalSpacing(
            16
        )

        grid.setVerticalSpacing(
            12
        )

        # -------------------------------------------------
        # MODO
        # -------------------------------------------------

        mode_label = QLabel(
            "Modo"
        )

        mode_label.setObjectName(
            "SecondaryText"
        )

        self.mode_combo = QComboBox()

        self.mode_combo.addItem(
            "Video completo",
            MODE_VIDEO
        )

        self.mode_combo.addItem(
            "Recorte",
            MODE_CLIP
        )

        self.mode_combo.addItem(
            "Solo audio (MP3)",
            MODE_AUDIO
        )

        self.mode_combo.currentIndexChanged.connect(
            self.on_mode_changed
        )

        grid.addWidget(
            mode_label,
            0,
            0
        )

        grid.addWidget(
            self.mode_combo,
            1,
            0
        )

        # -------------------------------------------------
        # CALIDAD
        # -------------------------------------------------

        quality_label = QLabel(
            "Calidad máxima"
        )

        quality_label.setObjectName(
            "SecondaryText"
        )

        self.quality_combo = QComboBox()

        self.quality_combo.addItem(
            "Mejor disponible",
            "best"
        )

        self.quality_combo.addItem(
            "1080p",
            "1080p"
        )

        self.quality_combo.addItem(
            "720p",
            "720p"
        )

        self.quality_combo.addItem(
            "480p",
            "480p"
        )

        self.quality_combo.setCurrentIndex(
            2
        )

        grid.addWidget(
            quality_label,
            0,
            1
        )

        grid.addWidget(
            self.quality_combo,
            1,
            1
        )

        # -------------------------------------------------
        # INICIO
        # -------------------------------------------------

        self.start_label = QLabel(
            "Inicio del recorte"
        )

        self.start_label.setObjectName(
            "SecondaryText"
        )

        self.start_input = QLineEdit(
            "00:00:10"
        )

        self.start_input.setPlaceholderText(
            "HH:MM:SS"
        )

        grid.addWidget(
            self.start_label,
            2,
            0
        )

        grid.addWidget(
            self.start_input,
            3,
            0
        )

        # -------------------------------------------------
        # FINAL
        # -------------------------------------------------

        self.end_label = QLabel(
            "Final del recorte"
        )

        self.end_label.setObjectName(
            "SecondaryText"
        )

        self.end_input = QLineEdit(
            "00:00:25"
        )

        self.end_input.setPlaceholderText(
            "HH:MM:SS"
        )

        grid.addWidget(
            self.end_label,
            2,
            1
        )

        grid.addWidget(
            self.end_input,
            3,
            1
        )

        layout.addLayout(
            grid
        )

        self.precise_cut_checkbox = QCheckBox(
            "Corte preciso "
            "(más lento, pero más exacto)"
        )

        self.precise_cut_checkbox.setChecked(
            True
        )

        layout.addWidget(
            self.precise_cut_checkbox
        )

        self.main_layout.addWidget(
            card
        )

        self.on_mode_changed()

    # =====================================================
    # DESTINO
    # =====================================================

    def build_destination_section(self):

        card, layout = (
            self.create_card()
        )

        title = QLabel(
            "CARPETA DE DESTINO"
        )

        title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            title
        )

        row = QHBoxLayout()

        self.folder_combo = QComboBox()

        self.folder_combo.setEditable(
            True
        )

        browse_button = QPushButton(
            "Examinar"
        )

        save_button = QPushButton(
            "Guardar ruta"
        )

        manage_button = QPushButton(
            "Administrar"
        )

        open_button = QPushButton(
            "Abrir"
        )

        browse_button.clicked.connect(
            self.browse_folder
        )

        save_button.clicked.connect(
            self.save_current_folder
        )

        manage_button.clicked.connect(
            self.manage_folders
        )

        open_button.clicked.connect(
            self.open_current_folder
        )

        row.addWidget(
            self.folder_combo,
            1
        )

        row.addWidget(
            browse_button
        )

        row.addWidget(
            save_button
        )

        row.addWidget(
            manage_button
        )

        row.addWidget(
            open_button
        )

        layout.addLayout(
            row
        )

        self.main_layout.addWidget(
            card
        )

        self.refresh_folders()

    # =====================================================
    # DESCARGA
    # =====================================================

    def build_download_section(self):

        card, layout = (
            self.create_card()
        )

        title = QLabel(
            "DESCARGAR / PROCESAR"
        )

        title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            title
        )

        buttons = QHBoxLayout()

        self.download_button = QPushButton(
            "Descargar"
        )

        self.download_button.setObjectName(
            "PrimaryButton"
        )

        self.cancel_button = QPushButton(
            "Cancelar"
        )

        self.cancel_button.setObjectName(
            "DangerButton"
        )

        self.cancel_button.setEnabled(
            False
        )

        self.download_button.clicked.connect(
            self.start_download
        )

        self.cancel_button.clicked.connect(
            self.cancel_download
        )

        buttons.addWidget(
            self.download_button
        )

        buttons.addWidget(
            self.cancel_button
        )

        buttons.addStretch()

        layout.addLayout(
            buttons
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange(
            0,
            100
        )

        self.progress_bar.setValue(
            0
        )

        layout.addWidget(
            self.progress_bar
        )

        self.download_status_label = QLabel(
            "Listo."
        )

        self.download_status_label.setObjectName(
            "StatusText"
        )

        layout.addWidget(
            self.download_status_label
        )

        self.log_box = QTextEdit()

        self.log_box.setReadOnly(
            True
        )

        self.log_box.setMinimumHeight(
            170
        )

        self.log_box.setPlaceholderText(
            "Aquí aparecerá el progreso técnico "
            "de yt-dlp y FFmpeg..."
        )

        layout.addWidget(
            self.log_box
        )

        self.main_layout.addWidget(
            card
        )

    # =====================================================
    # FOOTER
    # =====================================================

    def build_footer(
        self,
        root_layout
    ):

        footer = QLabel()

        footer.setObjectName(
            "FooterText"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setOpenExternalLinks(
            True
        )

        github = (
            f'<a style="color:#8D95A5; '
            f'text-decoration:none;" '
            f'href="{GITHUB_URL}">'
            f'GitHub</a>'
        )

        if LINKEDIN_URL:

            linkedin = (
                f'<a style="color:#8D95A5; '
                f'text-decoration:none;" '
                f'href="{LINKEDIN_URL}">'
                f'LinkedIn</a>'
            )

        else:

            linkedin = (
                '<span style="color:#5F6673;">'
                'LinkedIn'
                '</span>'
            )
        
       # if INSTAGRAM_URL:

          #  instagram = (
               # f'<a style="color:#8D95A5; '
                #f'text-decoration:none;" '
               # f'href="{INSTAGRAM_URL}">'
               # f'Instagram</a>'
          #  )

      #  else:

            #instagram = (
                #'<span style="color:#5F6673;">'
               # 'Instagram'
               # '</span>'
          #  )

        footer.setText(
            "Desarrollado por Deivy Jose"
            "&nbsp;&nbsp;·&nbsp;&nbsp;"
            f"{linkedin}"
            "&nbsp;&nbsp;·&nbsp;&nbsp;"
            f"{github}"
          #  "&nbsp;&nbsp;·&nbsp;&nbsp;"
          #  f"{instagram}"
        )

        root_layout.addWidget(
            footer
        )

    # =====================================================
    # MODO
    # =====================================================

    def on_mode_changed(
        self,
        _index=None
    ):

        mode = (
            self.mode_combo
            .currentData()
        )

        is_clip = (
            mode == MODE_CLIP
        )

        is_audio = (
            mode == MODE_AUDIO
        )

        self.start_label.setVisible(
            is_clip
        )

        self.start_input.setVisible(
            is_clip
        )

        self.end_label.setVisible(
            is_clip
        )

        self.end_input.setVisible(
            is_clip
        )

        self.precise_cut_checkbox.setVisible(
            is_clip
        )

        self.quality_combo.setEnabled(
            not is_audio
        )

    # =====================================================
    # BRAVE
    # =====================================================

    def save_brave_preference(
        self,
        checked: bool
    ):

        self.config.use_brave_cookies = (
            checked
        )

    # =====================================================
    # ANALIZAR
    # =====================================================

    def analyze_video(self):

        url = (
            self.url_input
            .text()
            .strip()
        )

        if not url:

            QMessageBox.warning(
                self,
                "Falta el enlace",
                "Pega primero un enlace de YouTube."
            )

            return

        if (
            self.analyze_worker is not None
            and
            self.analyze_worker.isRunning()
        ):
            return

        self.current_video_info = None

        self.analyze_button.setEnabled(
            False
        )

        self.video_title_label.setText(
            "Analizando video..."
        )

        self.channel_label.setText(
            "Canal: —"
        )

        self.duration_label.setText(
            "Duración: —"
        )

        self.video_status_label.setText(
            "Consultando información con yt-dlp..."
        )

        self.analyze_worker = (
            AnalyzeVideoWorker(
                url=url,

                use_brave_cookies=(
                    self.brave_checkbox
                    .isChecked()
                ),

                parent=self
            )
        )

        self.analyze_worker.success.connect(
            self.on_analyze_success
        )

        self.analyze_worker.error.connect(
            self.on_analyze_error
        )

        self.analyze_worker.finished.connect(
            self.on_analyze_finished
        )

        self.analyze_worker.start()

    def on_analyze_success(
        self,
        video_info
    ):

        self.current_video_info = (
            video_info
        )

        self.video_title_label.setText(
            video_info.title
        )

        self.channel_label.setText(
            f"Canal: {video_info.channel}"
        )

        self.duration_label.setText(
            f"Duración: {video_info.duration_text}"
        )

        self.video_status_label.setText(
            "Video analizado correctamente."
        )

    def on_analyze_error(
        self,
        message: str
    ):

        self.current_video_info = None

        self.video_title_label.setText(
            "No se pudo analizar el video."
        )

        self.channel_label.setText(
            "Canal: —"
        )

        self.duration_label.setText(
            "Duración: —"
        )

        self.video_status_label.setText(
            "Ocurrió un error durante el análisis."
        )

        QMessageBox.critical(
            self,
            "Error al analizar",
            message
        )

    def on_analyze_finished(self):

        self.analyze_button.setEnabled(
            True
        )

        if self.analyze_worker is not None:

            self.analyze_worker.deleteLater()

            self.analyze_worker = None

    # =====================================================
    # CARPETAS
    # =====================================================

    def refresh_folders(
        self,
        selected: str | None = None
    ):

        current = (
            selected
            or
            self.config.last_folder
        )

        self.folder_combo.blockSignals(
            True
        )

        self.folder_combo.clear()

        self.folder_combo.addItems(
            self.config.favorite_folders
        )

        if current:

            index = (
                self.folder_combo
                .findText(current)
            )

            if index >= 0:

                self.folder_combo.setCurrentIndex(
                    index
                )

            else:

                self.folder_combo.setEditText(
                    current
                )

        self.folder_combo.blockSignals(
            False
        )

    def current_folder(self) -> str:

        return (
            self.folder_combo
            .currentText()
            .strip()
        )

    def browse_folder(self):

        initial = (
            self.current_folder()
            or
            self.config.last_folder
        )

        folder = (
            QFileDialog.getExistingDirectory(
                self,
                "Seleccionar carpeta de destino",
                initial
            )
        )

        if not folder:
            return

        self.folder_combo.setEditText(
            folder
        )

        self.config.last_folder = (
            folder
        )

    def save_current_folder(self):

        folder = (
            self.current_folder()
        )

        if not folder:
            return

        path = (
            Path(folder)
            .expanduser()
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "La carpeta no existe",
                "Selecciona una carpeta existente "
                "antes de guardarla como favorita."
            )

            return

        folder = str(
            path.resolve()
        )

        self.config.add_favorite_folder(
            folder
        )

        self.config.last_folder = (
            folder
        )

        self.refresh_folders(
            folder
        )

        self.download_status_label.setText(
            "Ruta guardada como favorita."
        )

    def manage_folders(self):

        dialog = FolderManagerDialog(
            self.config,
            self
        )

        dialog.exec()

        self.refresh_folders()

    def open_current_folder(self):

        folder = (
            self.current_folder()
        )

        if not folder:
            return

        path = (
            Path(folder)
            .expanduser()
        )

        if not path.exists():

            QMessageBox.warning(
                self,
                "La carpeta no existe",
                "La ruta seleccionada no existe."
            )

            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(path.resolve())
            )
        )

    # =====================================================
    # VALIDAR DESCARGA
    # =====================================================

    def create_download_request(self):

        url = (
            self.url_input
            .text()
            .strip()
        )

        destination = (
            self.current_folder()
        )

        mode = (
            self.mode_combo
            .currentData()
        )

        quality = (
            self.quality_combo
            .currentData()
        )

        if not url:

            QMessageBox.warning(
                self,
                "Falta el enlace",
                "Pega primero un enlace."
            )

            return None

        if not destination:

            QMessageBox.warning(
                self,
                "Falta la carpeta",
                "Selecciona una carpeta de destino."
            )

            return None

        if mode == MODE_CLIP:

            try:

                start_seconds = (
                    time_to_seconds(
                        self.start_input.text()
                    )
                )

                end_seconds = (
                    time_to_seconds(
                        self.end_input.text()
                    )
                )

            except ValueError as error:

                QMessageBox.warning(
                    self,
                    "Tiempo inválido",
                    str(error)
                )

                return None

            if end_seconds <= start_seconds:

                QMessageBox.warning(
                    self,
                    "Tiempo inválido",
                    "El tiempo final debe ser mayor "
                    "que el tiempo inicial."
                )

                return None

            # Si analizamos previamente el video,
            # podemos validar también su duración.
            if (
                self.current_video_info is not None
                and
                self.current_video_info.duration > 0
                and
                end_seconds
                >
                self.current_video_info.duration
            ):

                QMessageBox.warning(
                    self,
                    "Tiempo fuera del video",
                    "El tiempo final supera "
                    "la duración del video."
                )

                return None

        self.config.last_folder = (
            destination
        )

        return DownloadRequest(
            url=url,

            destination=destination,

            mode=mode,

            quality=quality,

            start_time=(
                self.start_input
                .text()
                .strip()
            ),

            end_time=(
                self.end_input
                .text()
                .strip()
            ),

            precise_cut=(
                self.precise_cut_checkbox
                .isChecked()
            ),

            use_brave_cookies=(
                self.brave_checkbox
                .isChecked()
            )
        )

    # =====================================================
    # INICIAR DESCARGA
    # =====================================================

    def start_download(self):

        if (
            self.download_worker is not None
            and
            self.download_worker.isRunning()
        ):
            return

        request = (
            self.create_download_request()
        )

        if request is None:
            return

        self.log_box.clear()

        self.progress_bar.setValue(
            0
        )

        self.download_status_label.setText(
            "Preparando..."
        )

        self.set_download_busy(
            True
        )

        self.download_worker = (
            DownloadWorker(
                request,
                parent=self
            )
        )

        self.download_worker.progress.connect(
            self.progress_bar.setValue
        )

        self.download_worker.log.connect(
            self.append_log
        )

        self.download_worker.success.connect(
            self.on_download_success
        )

        self.download_worker.error.connect(
            self.on_download_error
        )

        self.download_worker.canceled.connect(
            self.on_download_canceled
        )

        self.download_worker.finished.connect(
            self.on_download_finished
        )

        self.download_worker.start()

    def append_log(
        self,
        text: str
    ):

        self.log_box.append(
            text
        )

        scrollbar = (
            self.log_box
            .verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

        self.download_status_label.setText(
            "Descargando / procesando..."
        )

    # =====================================================
    # CANCELAR
    # =====================================================

    def cancel_download(self):

        if (
            self.download_worker is None
            or
            not self.download_worker.isRunning()
        ):
            return

        self.download_status_label.setText(
            "Cancelando..."
        )

        self.download_worker.cancel()

    # =====================================================
    # RESULTADOS
    # =====================================================

    def on_download_success(
        self,
        destination: str
    ):

        self.progress_bar.setValue(
            100
        )

        self.download_status_label.setText(
            "Proceso completado correctamente."
        )

        QMessageBox.information(
            self,
            "Completado",
            "El archivo fue procesado correctamente.\n\n"
            f"Carpeta:\n{destination}"
        )

    def on_download_error(
        self,
        message: str
    ):

        self.download_status_label.setText(
            "Ocurrió un error."
        )

        QMessageBox.critical(
            self,
            "Error durante la descarga",
            message
        )

    def on_download_canceled(self):

        self.download_status_label.setText(
            "Proceso cancelado."
        )

    def on_download_finished(self):

        self.set_download_busy(
            False
        )

        if self.download_worker is not None:

            self.download_worker.deleteLater()

            self.download_worker = None

    # =====================================================
    # BLOQUEAR CONTROLES
    # =====================================================

    def set_download_busy(
        self,
        busy: bool
    ):

        self.download_button.setEnabled(
            not busy
        )

        self.cancel_button.setEnabled(
            busy
        )

        self.mode_combo.setEnabled(
            not busy
        )

        self.folder_combo.setEnabled(
            not busy
        )

        self.start_input.setEnabled(
            not busy
        )

        self.end_input.setEnabled(
            not busy
        )

        self.precise_cut_checkbox.setEnabled(
            not busy
        )

        self.brave_checkbox.setEnabled(
            not busy
        )

        self.analyze_button.setEnabled(
            not busy
        )

        if busy:

            self.quality_combo.setEnabled(
                False
            )

        else:

            self.on_mode_changed()

    # =====================================================
    # CERRAR APLICACIÓN
    # =====================================================

    def closeEvent(
        self,
        event: QCloseEvent
    ):

        if (
            self.download_worker is not None
            and
            self.download_worker.isRunning()
        ):

            answer = QMessageBox.question(
                self,

                "Descarga activa",

                "Hay una descarga en proceso.\n\n"
                "¿Quieres cancelarla y cerrar?",

                (
                    QMessageBox.StandardButton.Yes
                    |
                    QMessageBox.StandardButton.No
                ),

                QMessageBox.StandardButton.No
            )

            if (
                answer
                ==
                QMessageBox.StandardButton.No
            ):

                event.ignore()

                return

            self.download_worker.cancel()

            self.download_worker.wait(
                3000
            )

        event.accept()