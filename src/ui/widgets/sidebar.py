"""Sidebar navigation widget."""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QLabel, QButtonGroup,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class Sidebar(QFrame):
    """Sidebar navigation widget."""
    
    page_changed = pyqtSignal(int)
    
    PAGES = [
        ("💬", "Chat with AI"),
        ("🤖", "AI-to-AI Chat"),
        ("🖼️", "Image Generator"),
        ("🎬", "Video Generator"),
        ("⚙️", "Settings"),
        ("📝", "Feedback"),
        ("🔄", "Check Updates"),
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        title = QLabel("RoleAI")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #e94560;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("v1.6.0-beta")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #8a8a8a;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        for i, (icon, text) in enumerate(self.PAGES):
            btn = QPushButton(f"  {icon}  {text}")
            btn.setObjectName("navButton")
            btn.setCheckable(True)
            btn.setFont(QFont("Segoe UI", 11))
            btn.setCursor(Qt.PointingHandCursor)
            
            self.button_group.addButton(btn, i)
            layout.addWidget(btn)
            
            if i == 0:
                btn.setChecked(True)
        
        layout.addStretch()
        
        footer = QLabel("© 2024 RoleAI Team")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #666666;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        self.button_group.idClicked.connect(self.page_changed.emit)
    
    def set_current_page(self, index: int):
        """Set the current page."""
        button = self.button_group.button(index)
        if button:
            button.setChecked(True)
