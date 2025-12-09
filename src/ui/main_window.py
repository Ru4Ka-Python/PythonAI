"""Main application window."""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt

from .styles import StyleSheet
from .widgets.sidebar import Sidebar
from .pages import (
    ChatPage,
    AIToAIPage,
    ImageGeneratorPage,
    VideoGeneratorPage,
    SettingsPage,
    FeedbackPage,
    UpdatesPage,
)
from ..config import ConfigManager
from ..api import OpenAIClient, LumaAIClient


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.openai_client = None
        self.lumaai_client = None
        
        self.init_clients()
        self.setup_ui()
        self.apply_theme(self.config_manager.config.theme)
    
    def init_clients(self):
        """Initialize API clients."""
        config = self.config_manager.config
        
        try:
            self.openai_client = OpenAIClient(config.openai_api_key)
        except ImportError:
            self.openai_client = None
        
        try:
            self.lumaai_client = LumaAIClient(config.lumaai_api_key)
        except ImportError:
            self.lumaai_client = None
    
    def setup_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("RoleAI - AI Assistant")
        self.setMinimumSize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.on_page_changed)
        main_layout.addWidget(self.sidebar)
        
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack, 1)
        
        self.pages = []
        
        self.chat_page = ChatPage()
        self.setup_page(self.chat_page)
        self.stack.addWidget(self.chat_page)
        self.pages.append(self.chat_page)
        
        self.ai_to_ai_page = AIToAIPage()
        self.setup_page(self.ai_to_ai_page)
        self.stack.addWidget(self.ai_to_ai_page)
        self.pages.append(self.ai_to_ai_page)
        
        self.image_page = ImageGeneratorPage()
        self.setup_page(self.image_page)
        self.stack.addWidget(self.image_page)
        self.pages.append(self.image_page)
        
        self.video_page = VideoGeneratorPage()
        self.setup_page(self.video_page)
        self.stack.addWidget(self.video_page)
        self.pages.append(self.video_page)
        
        self.settings_page = SettingsPage()
        self.setup_page(self.settings_page)
        self.settings_page.settings_changed.connect(self.on_settings_changed)
        self.settings_page.theme_changed.connect(self.apply_theme)
        self.settings_page.load_settings()
        self.stack.addWidget(self.settings_page)
        self.pages.append(self.settings_page)
        
        self.feedback_page = FeedbackPage()
        self.setup_page(self.feedback_page)
        self.stack.addWidget(self.feedback_page)
        self.pages.append(self.feedback_page)
        
        self.updates_page = UpdatesPage()
        self.setup_page(self.updates_page)
        self.stack.addWidget(self.updates_page)
        self.pages.append(self.updates_page)
        
        if self.config_manager.config.auto_check_updates:
            self.updates_page.check_updates()
    
    def setup_page(self, page):
        """Setup common page properties."""
        page.set_config_manager(self.config_manager)
        page.set_openai_client(self.openai_client)
        page.set_lumaai_client(self.lumaai_client)
    
    def on_page_changed(self, index: int):
        """Handle page change."""
        self.stack.setCurrentIndex(index)
    
    def on_settings_changed(self):
        """Handle settings change."""
        config = self.config_manager.config
        
        if self.openai_client:
            self.openai_client.set_api_key(config.openai_api_key)
        
        if self.lumaai_client:
            self.lumaai_client.set_api_key(config.lumaai_api_key)
        
        for page in self.pages:
            page.set_openai_client(self.openai_client)
            page.set_lumaai_client(self.lumaai_client)
    
    def apply_theme(self, theme: str):
        """Apply theme to the application."""
        stylesheet = StyleSheet.get_theme(theme)
        self.setStyleSheet(stylesheet)
