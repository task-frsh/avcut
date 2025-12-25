"""
Main Window for AviCut
"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QLineEdit, QFileDialog, QStackedWidget,
    QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from src.ui.drop_zone import DropZone
from src.ui.file_list import FileListWidget
from src.ui.progress import ProgressWidget
from src.ui.result import ResultDialog
from src.core.splitter import VideoSplitter, BatchResult
from src.i18n import t, set_language, get_current_lang, get_manager


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self._splitter = VideoSplitter()
        self._worker = None
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Setup the UI."""
        self.setWindowTitle(t("app.title"))
        self.setMinimumSize(600, 500)
        self.resize(700, 550)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)

        title_label = QLabel(t("app.title"))
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Language toggle button
        self.lang_btn = QPushButton(t("language.toggle"))
        self.lang_btn.setObjectName("langBtn")
        self.lang_btn.clicked.connect(self._toggle_language)
        header_layout.addWidget(self.lang_btn)

        main_layout.addWidget(header)

        # Content area with stacked widget
        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")

        # Page 0: Main input page
        self.input_page = QWidget()
        self._setup_input_page()
        self.stack.addWidget(self.input_page)

        # Page 1: Progress page
        self.progress_widget = ProgressWidget()
        self.progress_widget.cancel_clicked.connect(self._cancel_split)
        self.stack.addWidget(self.progress_widget)

        main_layout.addWidget(self.stack)

    def _setup_input_page(self):
        """Setup the input page."""
        layout = QVBoxLayout(self.input_page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.files_added.connect(self._on_files_added)
        layout.addWidget(self.drop_zone)

        # File list
        self.file_list = FileListWidget()
        self.file_list.files_changed.connect(self._on_files_changed)
        self.file_list.hide()
        layout.addWidget(self.file_list)

        # Settings panel
        settings_frame = QFrame()
        settings_frame.setObjectName("settingsFrame")
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setSpacing(10)

        # Duration setting
        duration_layout = QHBoxLayout()

        self.duration_label = QLabel(t("label.duration"))
        self.duration_label.setObjectName("settingLabel")
        duration_layout.addWidget(self.duration_label)

        self.duration_spin = QSpinBox()
        self.duration_spin.setObjectName("durationSpin")
        self.duration_spin.setRange(1, 999)
        self.duration_spin.setValue(5)
        self.duration_spin.setSuffix(f" {t('format.minutes')}")
        duration_layout.addWidget(self.duration_spin)

        duration_layout.addStretch()
        settings_layout.addLayout(duration_layout)

        # Output folder setting
        output_layout = QHBoxLayout()

        self.output_label = QLabel(t("label.output"))
        self.output_label.setObjectName("settingLabel")
        output_layout.addWidget(self.output_label)

        self.output_edit = QLineEdit()
        self.output_edit.setObjectName("outputEdit")
        self.output_edit.setPlaceholderText(t("dialog.select_output"))
        # Set default output to user's Videos folder
        default_output = os.path.join(os.path.expanduser("~"), "Videos", "AviCut_Output")
        self.output_edit.setText(default_output)
        output_layout.addWidget(self.output_edit, stretch=1)

        self.browse_btn = QPushButton(t("btn.browse"))
        self.browse_btn.setObjectName("browseBtn")
        self.browse_btn.clicked.connect(self._browse_output)
        output_layout.addWidget(self.browse_btn)

        settings_layout.addLayout(output_layout)
        layout.addWidget(settings_frame)

        # Start button
        self.start_btn = QPushButton(t("btn.start"))
        self.start_btn.setObjectName("startBtn")
        self.start_btn.clicked.connect(self._start_split)
        self.start_btn.setEnabled(False)
        layout.addWidget(self.start_btn)

    def _apply_styles(self):
        """Apply application styles."""
        style = """
        QMainWindow {
            background-color: #1F2937;
        }

        #header {
            background-color: #111827;
            border-bottom: 1px solid #374151;
        }

        #titleLabel {
            color: #F9FAFB;
            font-size: 18px;
            font-weight: bold;
        }

        #langBtn {
            background-color: #374151;
            color: #F9FAFB;
            border: 1px solid #4B5563;
            border-radius: 4px;
            padding: 5px 15px;
            font-size: 12px;
        }

        #langBtn:hover {
            background-color: #4B5563;
        }

        #dropContainer {
            background-color: #374151;
            border: 2px dashed #4B5563;
            border-radius: 10px;
            min-height: 200px;
        }

        #dropContainer[dragging="true"] {
            border-color: #2563EB;
            background-color: #1E3A5F;
        }

        #plusIcon {
            color: #9CA3AF;
            font-size: 48px;
        }

        #instructionLabel {
            color: #9CA3AF;
            font-size: 16px;
        }

        #orLabel {
            color: #6B7280;
            font-size: 12px;
        }

        #selectFilesBtn, #selectFolderBtn {
            background-color: #2563EB;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            font-size: 14px;
        }

        #selectFilesBtn:hover, #selectFolderBtn:hover {
            background-color: #1D4ED8;
        }

        #settingsFrame {
            background-color: #374151;
            border-radius: 8px;
            padding: 15px;
        }

        #settingLabel {
            color: #D1D5DB;
            font-size: 14px;
            min-width: 150px;
        }

        #durationSpin {
            background-color: #1F2937;
            color: #F9FAFB;
            border: 1px solid #4B5563;
            border-radius: 4px;
            padding: 5px 10px;
            font-size: 14px;
            min-width: 100px;
        }

        #outputEdit {
            background-color: #1F2937;
            color: #F9FAFB;
            border: 1px solid #4B5563;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
        }

        #browseBtn {
            background-color: #4B5563;
            color: #F9FAFB;
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
        }

        #browseBtn:hover {
            background-color: #6B7280;
        }

        #startBtn {
            background-color: #10B981;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
        }

        #startBtn:hover {
            background-color: #059669;
        }

        #startBtn:disabled {
            background-color: #4B5563;
            color: #9CA3AF;
        }

        /* File list styles */
        #filesLabel, #totalDurationLabel {
            color: #D1D5DB;
            font-size: 13px;
        }

        #clearBtn {
            background-color: #EF4444;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 10px;
            font-size: 12px;
        }

        #clearBtn:hover {
            background-color: #DC2626;
        }

        #fileListScroll {
            background-color: #374151;
            border: 1px solid #4B5563;
            border-radius: 5px;
        }

        #fileItem {
            background-color: #1F2937;
            border-radius: 4px;
            margin: 2px;
        }

        #fileName {
            color: #F9FAFB;
            font-size: 13px;
        }

        #fileDuration {
            color: #9CA3AF;
            font-size: 12px;
        }

        #removeBtn {
            background-color: transparent;
            color: #EF4444;
            border: none;
            font-size: 16px;
            font-weight: bold;
        }

        #removeBtn:hover {
            color: #DC2626;
        }

        /* Progress styles */
        #statusLabel {
            color: #F9FAFB;
            font-size: 20px;
            font-weight: bold;
        }

        #currentFileLabel {
            color: #9CA3AF;
            font-size: 14px;
        }

        #overallLabel {
            color: #D1D5DB;
            font-size: 13px;
        }

        QProgressBar {
            background-color: #374151;
            border: none;
            border-radius: 5px;
            height: 20px;
            text-align: center;
            color: white;
        }

        QProgressBar::chunk {
            background-color: #2563EB;
            border-radius: 5px;
        }

        #cancelBtn {
            background-color: #EF4444;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 30px;
            font-size: 14px;
        }

        #cancelBtn:hover {
            background-color: #DC2626;
        }

        /* Result dialog styles */
        #resultDialog {
            background-color: #1F2937;
        }

        #resultTitle {
            color: #10B981;
            font-size: 24px;
            font-weight: bold;
        }

        #summaryFrame {
            background-color: #374151;
            border-radius: 8px;
            padding: 15px;
        }

        #summaryTitle {
            color: #F9FAFB;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        #summaryLabel {
            color: #9CA3AF;
            font-size: 13px;
        }

        #summaryValue {
            color: #F9FAFB;
            font-size: 13px;
            font-weight: bold;
        }

        #summaryValue[error="true"] {
            color: #EF4444;
        }

        #filesTitle {
            color: #D1D5DB;
            font-size: 14px;
            font-weight: bold;
        }

        #resultFilesScroll {
            background-color: #374151;
            border: 1px solid #4B5563;
            border-radius: 5px;
        }

        #outputFileLabel {
            color: #10B981;
            font-size: 12px;
        }

        #openFolderBtn, #splitMoreBtn {
            background-color: #2563EB;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
        }

        #openFolderBtn:hover, #splitMoreBtn:hover {
            background-color: #1D4ED8;
        }

        QScrollBar:vertical {
            background-color: #374151;
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background-color: #4B5563;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #6B7280;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
        self.setStyleSheet(style)

    def _toggle_language(self):
        """Toggle between English and Korean."""
        current = get_current_lang()
        new_lang = "ko" if current == "en" else "en"
        set_language(new_lang)
        self._update_all_texts()

    def _update_all_texts(self):
        """Update all UI texts after language change."""
        self.setWindowTitle(t("app.title"))
        self.lang_btn.setText(t("language.toggle"))

        # Update drop zone
        self.drop_zone.update_texts()

        # Update file list
        self.file_list.update_texts()

        # Update settings
        self.duration_label.setText(t("label.duration"))
        self.duration_spin.setSuffix(f" {t('format.minutes')}")
        self.output_label.setText(t("label.output"))
        self.output_edit.setPlaceholderText(t("dialog.select_output"))
        self.browse_btn.setText(t("btn.browse"))

        # Update buttons
        self.start_btn.setText(t("btn.start"))

        # Update progress widget
        self.progress_widget.update_texts()

    def _on_files_added(self, files):
        """Handle files added."""
        self.file_list.add_files(files)

        if not self.file_list.is_empty():
            self.drop_zone.hide()
            self.file_list.show()
            self.start_btn.setEnabled(True)

    def _on_files_changed(self, files):
        """Handle file list changed."""
        if len(files) == 0:
            self.file_list.hide()
            self.drop_zone.show()
            self.start_btn.setEnabled(False)

    def _browse_output(self):
        """Browse for output folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            t("dialog.select_output"),
            self.output_edit.text()
        )
        if folder:
            self.output_edit.setText(folder)

    def _start_split(self):
        """Start the splitting process."""
        # Validate
        files = self.file_list.get_files()
        if not files:
            QMessageBox.warning(self, t("status.error"), t("error.no_files"))
            return

        output_dir = self.output_edit.text()
        if not output_dir:
            QMessageBox.warning(self, t("status.error"), t("error.no_output"))
            return

        duration = self.duration_spin.value()
        if duration <= 0:
            QMessageBox.warning(self, t("status.error"), t("error.invalid_duration"))
            return

        # Check FFmpeg
        if not self._splitter.is_ffmpeg_available():
            QMessageBox.critical(self, t("status.error"), t("error.ffmpeg_not_found"))
            return

        # Switch to progress view
        self.stack.setCurrentIndex(1)
        self.progress_widget.reset()

        # Create and start worker
        self._worker = self._splitter.create_worker(files, duration, output_dir)
        self._worker.progress.connect(self._on_progress)
        self._worker.all_complete.connect(self._on_complete)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _cancel_split(self):
        """Cancel the splitting process."""
        if self._worker:
            self._worker.cancel()
            self.progress_widget.set_cancelled()

    def _on_progress(self, current_file, total_files, filename, file_progress):
        """Handle progress update."""
        self.progress_widget.update_progress(current_file, total_files, filename, file_progress)

    def _on_complete(self, result: BatchResult):
        """Handle split complete."""
        self._worker = None

        # Show result dialog
        dialog = ResultDialog(result, self.output_edit.text(), self)
        dialog.exec()

        # Return to input view
        self.stack.setCurrentIndex(0)
        self.file_list.clear_all()
        self.drop_zone.show()
        self.file_list.hide()
        self.start_btn.setEnabled(False)

    def _on_error(self, message):
        """Handle error."""
        self._worker = None
        self.progress_widget.set_error(message)
        QMessageBox.critical(self, t("status.error"), message)
        self.stack.setCurrentIndex(0)
