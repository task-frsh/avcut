"""
Drag & Drop Zone Widget for AviCut
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

from src.core.utils import is_video_file, get_video_files_from_folder
from src.i18n import t


class DropZone(QWidget):
    """Widget for drag & drop file selection."""

    files_added = pyqtSignal(list)  # List of file paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Drop area container
        self.drop_container = QWidget()
        self.drop_container.setObjectName("dropContainer")
        drop_layout = QVBoxLayout(self.drop_container)
        drop_layout.setSpacing(15)

        # Plus icon
        self.plus_label = QLabel("+")
        self.plus_label.setObjectName("plusIcon")
        self.plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(self.plus_label)

        # Instruction text
        self.instruction_label = QLabel(t("drop.instruction"))
        self.instruction_label.setObjectName("instructionLabel")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(self.instruction_label)

        # Or label
        self.or_label = QLabel(t("drop.or"))
        self.or_label.setObjectName("orLabel")
        self.or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(self.or_label)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.select_files_btn = QPushButton(t("btn.select_files"))
        self.select_files_btn.setObjectName("selectFilesBtn")
        self.select_files_btn.clicked.connect(self._on_select_files)
        btn_layout.addWidget(self.select_files_btn)

        self.select_folder_btn = QPushButton(t("btn.select_folder"))
        self.select_folder_btn.setObjectName("selectFolderBtn")
        self.select_folder_btn.clicked.connect(self._on_select_folder)
        btn_layout.addWidget(self.select_folder_btn)

        drop_layout.addLayout(btn_layout)
        layout.addWidget(self.drop_container)

    def update_texts(self):
        """Update texts for language change."""
        self.instruction_label.setText(t("drop.instruction"))
        self.or_label.setText(t("drop.or"))
        self.select_files_btn.setText(t("btn.select_files"))
        self.select_folder_btn.setText(t("btn.select_folder"))

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_container.setProperty("dragging", True)
            self.drop_container.style().unpolish(self.drop_container)
            self.drop_container.style().polish(self.drop_container)

    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.drop_container.setProperty("dragging", False)
        self.drop_container.style().unpolish(self.drop_container)
        self.drop_container.style().polish(self.drop_container)

    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        self.drop_container.setProperty("dragging", False)
        self.drop_container.style().unpolish(self.drop_container)
        self.drop_container.style().polish(self.drop_container)

        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if is_video_file(path):
                files.append(path)
            elif path and not path.endswith(('.lnk',)):
                # Check if it's a folder
                folder_files = get_video_files_from_folder(path)
                files.extend(folder_files)

        if files:
            self.files_added.emit(files)
            event.acceptProposedAction()

    def _on_select_files(self):
        """Handle select files button click."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            t("dialog.select_files"),
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.webm *.wmv *.flv *.m4v *.mpeg *.mpg);;All Files (*)"
        )
        if files:
            self.files_added.emit(files)

    def _on_select_folder(self):
        """Handle select folder button click."""
        folder = QFileDialog.getExistingDirectory(
            self,
            t("dialog.select_folder"),
            ""
        )
        if folder:
            files = get_video_files_from_folder(folder)
            if files:
                self.files_added.emit(files)
