#!/usr/bin/env python3
"""RoleAI - A PyQt5 AI Assistant Application.

Main entry point for the application.
"""

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.ui import MainWindow


def main():
    """Main application entry point."""
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("RoleAI")
    app.setApplicationVersion("1.6.0-beta")
    app.setOrganizationName("RoleAI Team")
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
