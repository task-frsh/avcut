"""
Progress Widget for AviCut
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.i18n import t


class ProgressWidget(QWidget):
    """Widget for displaying split progress."""

    cancel_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Status label
        self.status_label = QLabel(t("status.processing"))
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Current file label
        self.file_label = QLabel("")
        self.file_label.setObjectName("currentFileLabel")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)

        # File progress bar
        self.file_progress = QProgressBar()
        self.file_progress.setObjectName("fileProgressBar")
        self.file_progress.setRange(0, 100)
        self.file_progress.setValue(0)
        self.file_progress.setTextVisible(True)
        layout.addWidget(self.file_progress)

        # Overall progress label
        self.overall_label = QLabel("0 / 0")
        self.overall_label.setObjectName("overallLabel")
        self.overall_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.overall_label)

        # Overall progress bar
        self.overall_progress = QProgressBar()
        self.overall_progress.setObjectName("overallProgressBar")
        self.overall_progress.setRange(0, 100)
        self.overall_progress.setValue(0)
        self.overall_progress.setTextVisible(True)
        layout.addWidget(self.overall_progress)

        # Cancel button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton(t("btn.cancel"))
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)
        btn_layout.addWidget(self.cancel_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

    def update_texts(self):
        """Update texts for language change."""
        self.status_label.setText(t("status.processing"))
        self.cancel_btn.setText(t("btn.cancel"))

    def reset(self):
        """Reset progress display."""
        self.file_progress.setValue(0)
        self.overall_progress.setValue(0)
        self.file_label.setText("")
        self.overall_label.setText("0 / 0")
        self.status_label.setText(t("status.processing"))
        self.cancel_btn.show()

    def update_progress(self, current_file: int, total_files: int, filename: str, file_progress: float):
        """Update progress display.

        Args:
            current_file: Current file number (1-indexed)
            total_files: Total number of files
            filename: Current filename
            file_progress: Progress of current file (0.0 to 1.0)
        """
        # Update file info
        self.file_label.setText(filename)

        # Update file progress
        self.file_progress.setValue(int(file_progress * 100))

        # Update overall progress
        self.overall_label.setText(f"{current_file} / {total_files}")
        overall = ((current_file - 1) + file_progress) / total_files
        self.overall_progress.setValue(int(overall * 100))

    def set_complete(self):
        """Set progress to complete state."""
        self.status_label.setText(t("status.complete"))
        self.file_progress.setValue(100)
        self.overall_progress.setValue(100)
        self.cancel_btn.hide()

    def set_cancelled(self):
        """Set progress to cancelled state."""
        self.status_label.setText(t("status.cancelled"))
        self.cancel_btn.hide()

    def set_error(self, message: str):
        """Set progress to error state."""
        self.status_label.setText(f"{t('status.error')}: {message}")
        self.cancel_btn.hide()
