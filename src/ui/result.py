"""
Result Dialog for AviCut
"""
import os
import subprocess
import sys
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt6.QtCore import Qt

from src.core.splitter import BatchResult
from src.i18n import t


class ResultDialog(QDialog):
    """Dialog for displaying split results."""

    def __init__(self, result: BatchResult, output_dir: str, parent=None):
        super().__init__(parent)
        self.result = result
        self.output_dir = output_dir
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI."""
        self.setWindowTitle(t("result.title"))
        self.setMinimumSize(500, 400)
        self.setObjectName("resultDialog")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title with checkmark
        title_label = QLabel(f"✓ {t('result.title')}")
        title_label.setObjectName("resultTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Summary section
        summary_frame = QFrame()
        summary_frame.setObjectName("summaryFrame")
        summary_layout = QVBoxLayout(summary_frame)

        summary_title = QLabel(t("result.summary"))
        summary_title.setObjectName("summaryTitle")
        summary_layout.addWidget(summary_title)

        # Summary details
        details = [
            (t("result.total_files"), str(self.result.total_files)),
            (t("result.successful"), str(self.result.successful)),
            (t("result.failed"), str(self.result.failed)),
            (t("result.segments"), str(self.result.total_segments)),
        ]

        for label_text, value in details:
            row = QHBoxLayout()
            label = QLabel(f"  {label_text}:")
            label.setObjectName("summaryLabel")
            row.addWidget(label)

            value_label = QLabel(value)
            value_label.setObjectName("summaryValue")
            if label_text == t("result.failed") and int(value) > 0:
                value_label.setProperty("error", True)
            row.addWidget(value_label)
            row.addStretch()

            summary_layout.addLayout(row)

        layout.addWidget(summary_frame)

        # Output files section
        files_label = QLabel(t("result.output_files"))
        files_label.setObjectName("filesTitle")
        layout.addWidget(files_label)

        # Scroll area for file list
        scroll_area = QScrollArea()
        scroll_area.setObjectName("resultFilesScroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(200)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(2)

        # Add file entries
        for res in self.result.results:
            for output_file in res.output_files:
                filename = os.path.basename(output_file)
                file_label = QLabel(f"✓ {filename}")
                file_label.setObjectName("outputFileLabel")
                file_label.setToolTip(output_file)
                scroll_layout.addWidget(file_label)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.open_folder_btn = QPushButton(t("btn.open_folder"))
        self.open_folder_btn.setObjectName("openFolderBtn")
        self.open_folder_btn.clicked.connect(self._open_output_folder)
        btn_layout.addWidget(self.open_folder_btn)

        self.split_more_btn = QPushButton(t("btn.split_more"))
        self.split_more_btn.setObjectName("splitMoreBtn")
        self.split_more_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.split_more_btn)

        layout.addLayout(btn_layout)

    def _open_output_folder(self):
        """Open the output folder in file explorer."""
        if sys.platform == 'win32':
            os.startfile(self.output_dir)
        elif sys.platform == 'darwin':
            subprocess.run(['open', self.output_dir])
        else:
            subprocess.run(['xdg-open', self.output_dir])
