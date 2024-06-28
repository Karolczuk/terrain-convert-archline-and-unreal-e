"""
Main file. Initializes the application window with functions
"""
import sys
from PySide6.QtWidgets import QApplication
from gui.converter_window import ConverterWindow

if __name__ == "__main__":
    app = QApplication()
    konverter = ConverterWindow()
    sys.exit(app.exec())