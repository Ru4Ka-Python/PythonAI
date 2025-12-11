"""Top navigation bar widget."""

from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QPushButton, QLabel, QButtonGroup,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class TopBar(QFrame):
    """Top navigation bar widget."""
    
    mode_changed = pyqtSignal(int)
    
    MODES = [
        ("💬", "Chat"),
        ("🤖", "AI-to-AI"),
        ("⚖️", "Compare AI"),
        ("🖼️", "Image"),
        ("🎬", "Video"),
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(10)
        
        # Logo/Title
        title = QLabel("RoleAI")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #e94560;")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        for i, (icon, text) in enumerate(self.MODES):
            btn = QPushButton(f"{icon} {text}")
            btn.setObjectName("topBarButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            
            self.button_group.addButton(btn, i)
            layout.addWidget(btn)
            
            if i == 0:
                btn.setChecked(True)
        
        layout.addStretch()
        
        # Version info or user info could go here
        
        self.button_group.idClicked.connect(self.mode_changed.emit)
        
    def set_current_mode(self, index: int):
        """Set the current mode."""
        button = self.button_group.button(index)
        if button:
            button.setChecked(True)
