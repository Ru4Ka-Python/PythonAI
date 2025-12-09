"""Base page class for all pages."""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class BasePage(QWidget):
    """Base class for all pages."""
    
    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.title_text = title
        self.subtitle_text = subtitle
        self._config_manager = None
        self._openai_client = None
        self._lumaai_client = None
    
    def set_config_manager(self, config_manager):
        """Set the configuration manager."""
        self._config_manager = config_manager
    
    def set_openai_client(self, client):
        """Set the OpenAI client."""
        self._openai_client = client
    
    def set_lumaai_client(self, client):
        """Set the LumaAI client."""
        self._lumaai_client = client
    
    @property
    def config(self):
        """Get current configuration."""
        if self._config_manager:
            return self._config_manager.config
        return None
    
    def create_header(self) -> QVBoxLayout:
        """Create a standard page header."""
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        title = QLabel(self.title_text)
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(title)
        
        if self.subtitle_text:
            subtitle = QLabel(self.subtitle_text)
            subtitle.setObjectName("subtitleLabel")
            subtitle.setFont(QFont("Segoe UI", 12))
            layout.addWidget(subtitle)
        
        return layout
    
    def show_error(self, title: str, message: str):
        """Show an error message box."""
        QMessageBox.critical(self, title, message)
    
    def show_info(self, title: str, message: str):
        """Show an info message box."""
        QMessageBox.information(self, title, message)
    
    def show_warning(self, title: str, message: str):
        """Show a warning message box."""
        QMessageBox.warning(self, title, message)
