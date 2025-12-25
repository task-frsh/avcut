"""
AviCut - Video Splitter
Main entry point
"""
import sys
import os

def setup_path():
    """Setup Python path for imports."""
    # Get the src directory
    src_dir = os.path.dirname(os.path.abspath(__file__))

    # For frozen exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
        sys.path.insert(0, base_path)
    else:
        # For development - add src to path
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

setup_path()

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Import with absolute imports
from src.ui.main_window import MainWindow


def main():
    """Main entry point."""
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("AviCut")
    app.setApplicationVersion("1.0.0")

    # Set app icon if available
    src_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(src_dir, '..', 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
