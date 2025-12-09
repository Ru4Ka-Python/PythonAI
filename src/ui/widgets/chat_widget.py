"""Chat widget components."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QSizePolicy, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class MessageBubble(QFrame):
    """A chat message bubble widget."""
    
    def __init__(self, message: str, is_user: bool = False, sender_name: str = "", parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setup_ui(message, sender_name)
    
    def setup_ui(self, message: str, sender_name: str):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        if sender_name:
            name_label = QLabel(sender_name)
            name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            name_label.setStyleSheet("color: #e94560;" if not self.is_user else "color: #ffffff;")
            layout.addWidget(name_label)
        
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_label.setFont(QFont("Segoe UI", 11))
        
        if self.is_user:
            self.setObjectName("chatBubbleUser")
            message_label.setStyleSheet("color: white;")
        else:
            self.setObjectName("chatBubbleAI")
            message_label.setStyleSheet("color: #eaeaea;")
        
        layout.addWidget(message_label)
        
        self.setMaximumWidth(600)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)


class ChatWidget(QWidget):
    """Widget for displaying chat messages."""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(20, 20, 20, 20)
        self.messages_layout.setSpacing(15)
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_container)
        layout.addWidget(self.scroll_area)
    
    def add_message(self, message: str, is_user: bool = False, sender_name: str = ""):
        """Add a message to the chat."""
        bubble = MessageBubble(message, is_user, sender_name)
        
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        if is_user:
            container_layout.addStretch()
            container_layout.addWidget(bubble)
        else:
            container_layout.addWidget(bubble)
            container_layout.addStretch()
        
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, container)
        self.messages.append({"role": "user" if is_user else "assistant", "content": message})
        
        self.scroll_to_bottom()
    
    def update_last_message(self, content: str):
        """Update the content of the last message (for streaming)."""
        if self.messages_layout.count() > 1:
            last_container = self.messages_layout.itemAt(self.messages_layout.count() - 2).widget()
            if last_container:
                bubble = last_container.findChild(MessageBubble)
                if bubble:
                    message_label = bubble.findChild(QLabel)
                    if message_label and not isinstance(message_label.text(), str) or message_label:
                        labels = bubble.findChildren(QLabel)
                        if labels:
                            labels[-1].setText(content)
        
        if self.messages:
            self.messages[-1]["content"] = content
        
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat."""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_messages(self):
        """Clear all messages."""
        while self.messages_layout.count() > 1:
            item = self.messages_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.messages.clear()
    
    def get_messages(self):
        """Get all messages."""
        return self.messages.copy()
