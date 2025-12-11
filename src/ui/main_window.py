"""Main application window."""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QLabel, QGraphicsOpacityEffect, QFrame
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint

from .styles import StyleSheet
from .widgets.topbar import TopBar
from .widgets.history_sidebar import HistorySidebar
from .pages import (
    ChatPage,
    AIToAIPage,
    CompareAIPage,
    ImageGeneratorPage,
    VideoGeneratorPage,
    SettingsPage,
    FeedbackPage,
    UpdatesPage,
)
from ..config import ConfigManager
from ..api.llm_client import LLMClient
from ..api.lumaai_client import LumaAIClient
from ..history_manager import HistoryManager

class ToastNotification(QLabel):
    """Simple toast notification."""
    def __init__(self, parent, text):
        super().__init__(text, parent)
        self.setStyleSheet("""
            background-color: #323232; 
            color: white; 
            padding: 12px 24px; 
            border-radius: 4px;
            font-family: 'Segoe UI';
            font-size: 14px;
        """)
        self.adjustSize()
        self.setAlignment(Qt.AlignCenter)
        self.hide()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_toast)
        
    def show_message(self, text, duration=3000):
        self.setText(text)
        self.adjustSize()
        # Center horizontally, near bottom
        parent_rect = self.parent().rect()
        x = (parent_rect.width() - self.width()) // 2
        y = parent_rect.height() - 100
        self.move(x, y)
        
        self.show()
        self.raise_()
        
        # Fade in
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()
        self.anim = anim # keep ref
        
        self.timer.start(duration)
        
    def hide_toast(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(300)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.finished.connect(self.hide)
        anim.start()
        self.anim_out = anim # keep ref
        self.timer.stop()

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.history_manager = HistoryManager()
        self.llm_client = None
        self.lumaai_client = None
        
        self.init_clients()
        self.setup_ui()
        self.apply_theme(self.config_manager.config.theme)
        
    def init_clients(self):
        """Initialize API clients."""
        config = self.config_manager.config
        
        self.llm_client = LLMClient(config.openai_api_key, config.gemini_api_key)
        
        try:
            self.lumaai_client = LumaAIClient(config.lumaai_api_key)
        except ImportError:
            self.lumaai_client = None
            
    def setup_ui(self):
        """Initialize the UI."""
        self.setWindowTitle("RoleAI - AI Assistant")
        self.setMinimumSize(1200, 800)
        
        # Main Layout: TopBar + (Sidebar | Content)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top Bar
        self.topbar = TopBar()
        self.topbar.mode_changed.connect(self.on_mode_changed)
        main_layout.addWidget(self.topbar)
        
        # Content Area (Sidebar + Stack)
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # History Sidebar
        self.history_sidebar = HistorySidebar()
        self.history_sidebar.item_clicked.connect(self.on_history_item_clicked)
        self.history_sidebar.item_renamed.connect(self.on_history_renamed)
        self.history_sidebar.item_deleted.connect(self.on_history_deleted)
        self.history_sidebar.settings_clicked.connect(self.open_settings)
        content_layout.addWidget(self.history_sidebar)
        
        # Stacked Widget
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack, 1)
        
        main_layout.addWidget(content_widget, 1)
        
        # Toast
        self.toast = ToastNotification(central_widget, "")
        
        self.pages = []
        
        # 0: Chat
        self.chat_page = ChatPage()
        self.add_page(self.chat_page)
        
        # 1: AI to AI
        self.ai_to_ai_page = AIToAIPage()
        self.add_page(self.ai_to_ai_page)
        
        # 2: Compare AI
        self.compare_ai_page = CompareAIPage()
        self.add_page(self.compare_ai_page)
        
        # 3: Image
        self.image_page = ImageGeneratorPage()
        self.add_page(self.image_page)
        
        # 4: Video
        self.video_page = VideoGeneratorPage()
        self.add_page(self.video_page)
        
        # Hidden Pages (Not in TopBar index)
        self.settings_page = SettingsPage()
        self.setup_page_dependencies(self.settings_page)
        self.settings_page.settings_changed.connect(self.on_settings_changed)
        self.settings_page.theme_changed.connect(self.apply_theme)
        self.settings_page.load_settings()
        self.stack.addWidget(self.settings_page)
        self.pages.append(self.settings_page)
        
        self.feedback_page = FeedbackPage()
        self.setup_page_dependencies(self.feedback_page)
        self.stack.addWidget(self.feedback_page)
        self.pages.append(self.feedback_page)
        
        self.updates_page = UpdatesPage()
        self.setup_page_dependencies(self.updates_page)
        self.stack.addWidget(self.updates_page)
        self.pages.append(self.updates_page)
        
        # Initialize first view
        self.on_mode_changed(0)
        
        if self.config_manager.config.auto_check_updates:
            self.updates_page.check_updates()
            
    def add_page(self, page):
        self.setup_page_dependencies(page)
        self.stack.addWidget(page)
        self.pages.append(page)
        
    def setup_page_dependencies(self, page):
        page.set_config_manager(self.config_manager)
        page.set_history_manager(self.history_manager)
        page.set_llm_client(self.llm_client)
        page.set_lumaai_client(self.lumaai_client)
        
    def on_mode_changed(self, index: int):
        # Fade out
        self.fade_transition(lambda: self.switch_mode_content(index))
        
    def switch_mode_content(self, index):
        self.stack.setCurrentIndex(index)
        
        # Map index to history mode
        mode_map = {
            0: "chat",
            1: "ai_to_ai",
            2: "compare_ai",
            3: "image",
            4: "video"
        }
        
        if index in mode_map:
            mode = mode_map[index]
            items = self.history_manager.get_items(mode)
            self.history_sidebar.update_history(mode.replace("_", " ").title(), items)
            self.history_sidebar.current_mode = mode
            self.history_sidebar.show()
        else:
             # Should not happen for topbar modes
             pass
             
    def fade_transition(self, callback):
        current = self.stack.currentWidget()
        if not current:
            callback()
            return
            
        effect = QGraphicsOpacityEffect(current)
        current.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(200)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.InQuad)
        anim.finished.connect(lambda: [callback(), self.fade_in_new()])
        anim.start()
        self.anim = anim
        
    def fade_in_new(self):
        new_widget = self.stack.currentWidget()
        effect = QGraphicsOpacityEffect(new_widget)
        new_widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(200)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
        self.anim_in = anim
        
    def on_history_item_clicked(self, item_id: str):
        mode = self.history_sidebar.current_mode
        item = self.history_manager.get_item(mode, item_id)
        if item:
            # Load data into current page
            page = self.stack.currentWidget()
            if hasattr(page, 'load_history_data'):
                page.load_history_data(item['data'])
                self.toast.show_message(f"Loaded: {item['name']}")
                
    def on_history_renamed(self, item_id: str, new_name: str):
        mode = self.history_sidebar.current_mode
        if self.history_manager.rename_item(mode, item_id, new_name):
            self.toast.show_message("Item renamed")
            
    def on_history_deleted(self, item_id: str):
        mode = self.history_sidebar.current_mode
        if self.history_manager.delete_item(mode, item_id):
            # Refresh list
            items = self.history_manager.get_items(mode)
            self.history_sidebar.update_history(mode.replace("_", " ").title(), items)
            self.toast.show_message("Item deleted")
            
    def open_settings(self):
        # Index of SettingsPage is 5
        self.stack.setCurrentIndex(5)
        # Maybe hide history sidebar or show settings history?
        # Requirement: "Settings section: Add the ability to change the system-installed font"
        # Requirement: "keep the 'Settings' section in the same place where it originally was" (Sidebar button)
        
    def on_settings_changed(self):
        config = self.config_manager.config
        
        if self.llm_client:
            self.llm_client.set_api_keys(config.openai_api_key, config.gemini_api_key)
        
        if self.lumaai_client:
            self.lumaai_client.set_api_key(config.lumaai_api_key)
            
        self.apply_theme(config.theme)
        
    def apply_theme(self, theme: str):
        stylesheet = StyleSheet.get_theme(theme, self.config_manager.config.font_family)
        self.setStyleSheet(stylesheet)
        
        # Propagate font change to app
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QFont
        app = QApplication.instance()
        if app:
            app.setFont(QFont(self.config_manager.config.font_family, 10))

    def resizeEvent(self, event):
        # Reposition toast if visible
        if hasattr(self, 'toast') and self.toast.isVisible():
            parent_rect = self.centralWidget().rect()
            x = (parent_rect.width() - self.toast.width()) // 2
            y = parent_rect.height() - 100
            self.toast.move(x, y)
        super().resizeEvent(event)
