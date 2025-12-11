#!/usr/bin/env python3
"""RoleAI - A PyQt5 AI Assistant Application.

Main entry point for the application.
"""

import sys
import os
import importlib.util

def check_dependencies():
    """Check if required libraries are installed."""
    required = {
        "PyQt5": "PyQt5",
        "openai": "openai",
        "requests": "requests",
        "aiohttp": "aiohttp",
        "markdown": "markdown",
        "pyperclip": "pyperclip",
        "google.generativeai": "google.generativeai"
    }
    
    missing = []
    
    for package, module in required.items():
        try:
            parts = module.split('.')
            if importlib.util.find_spec(parts[0]) is None:
                missing.append(package)
        except Exception:
            missing.append(package)
            
    return missing

def main():
    """Main application entry point."""
    missing = check_dependencies()
    if missing:
        print(f"Error: Missing required libraries: {', '.join(missing)}")
        print("Please run: pip install -r requirements.txt")
        # Try to show a GUI error if possible (e.g. via tkinter if PyQt is missing)
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", 
                                 f"Missing libraries:\n{', '.join(missing)}\n\nPlease run: pip install -r requirements.txt")
            return
        except ImportError:
            pass
            
        if "PyQt5" in missing:
            sys.exit(1)

    # Late import to ensure dependencies are checked first
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    from src.ui.main_window import MainWindow
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("RoleAI")
    app.setApplicationVersion("1.6.0-beta")
    app.setOrganizationName("RoleAI Team")
    
    # Font will be handled by Config/Theme, but set a sane default
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
