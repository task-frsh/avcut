"""
File List Widget for AviCut
"""
import os
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.core.utils import format_duration
from src.core.splitter import VideoSplitter
from src.i18n import t


class FileItem(QFrame):
    """Single file item widget."""

    remove_clicked = pyqtSignal(str)  # file path

    def __init__(self, file_path: str, duration: float, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.duration = duration
        self.setObjectName("fileItem")
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        # File name
        filename = os.path.basename(self.file_path)
        self.name_label = QLabel(filename)
        self.name_label.setObjectName("fileName")
        self.name_label.setToolTip(self.file_path)
        layout.addWidget(self.name_label, stretch=1)

        # Duration
        self.duration_label = QLabel(format_duration(self.duration))
        self.duration_label.setObjectName("fileDuration")
        layout.addWidget(self.duration_label)

        # Remove button
        self.remove_btn = QPushButton("×")
        self.remove_btn.setObjectName("removeBtn")
        self.remove_btn.setFixedSize(24, 24)
        self.remove_btn.clicked.connect(lambda: self.remove_clicked.emit(self.file_path))
        layout.addWidget(self.remove_btn)


class FileListWidget(QWidget):
    """Widget for displaying list of added files."""

    files_changed = pyqtSignal(list)  # List of file paths

    def __init__(self, parent=None):
        super().__init__(parent)
        self._files: Dict[str, float] = {}  # path -> duration
        self._splitter = VideoSplitter()
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()

        self.files_label = QLabel(f"{t('label.files')}: 0")
        self.files_label.setObjectName("filesLabel")
        header_layout.addWidget(self.files_label)

        header_layout.addStretch()

        self.total_duration_label = QLabel(f"{t('label.total_duration')}: 00:00")
        self.total_duration_label.setObjectName("totalDurationLabel")
        header_layout.addWidget(self.total_duration_label)

        self.clear_btn = QPushButton(t("btn.clear_all"))
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.hide()
        header_layout.addWidget(self.clear_btn)

        layout.addLayout(header_layout)

        # Scroll area for file items
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("fileListScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

    def update_texts(self):
        """Update texts for language change."""
        self._update_header()
        self.clear_btn.setText(t("btn.clear_all"))

    def add_files(self, file_paths: List[str]):
        """Add files to the list."""
        for path in file_paths:
            if path not in self._files:
                # Get duration
                duration = self._splitter.get_video_duration(path)
                self._files[path] = duration

                # Create file item
                item = FileItem(path, duration)
                item.remove_clicked.connect(self._remove_file)

                # Insert before stretch
                self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item)

        self._update_header()
        self.files_changed.emit(list(self._files.keys()))

    def _remove_file(self, file_path: str):
        """Remove a file from the list."""
        if file_path in self._files:
            del self._files[file_path]

            # Find and remove widget
            for i in range(self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, FileItem) and widget.file_path == file_path:
                        widget.deleteLater()
                        break

            self._update_header()
            self.files_changed.emit(list(self._files.keys()))

    def clear_all(self):
        """Clear all files."""
        self._files.clear()

        # Remove all file items
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._update_header()
        self.files_changed.emit([])

    def get_files(self) -> List[str]:
        """Get list of file paths."""
        return list(self._files.keys())

    def get_total_duration(self) -> float:
        """Get total duration of all files."""
        return sum(self._files.values())

    def file_count(self) -> int:
        """Get number of files."""
        return len(self._files)

    def _update_header(self):
        """Update header labels."""
        count = len(self._files)
        total = sum(self._files.values())

        self.files_label.setText(f"{t('label.files')}: {count}")
        self.total_duration_label.setText(f"{t('label.total_duration')}: {format_duration(total)}")

        if count > 0:
            self.clear_btn.show()
        else:
            self.clear_btn.hide()

    def is_empty(self) -> bool:
        """Check if file list is empty."""
        return len(self._files) == 0
