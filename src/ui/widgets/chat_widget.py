"""Chat widget components."""

import re
import markdown
import pyperclip
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QSizePolicy, QTextBrowser, QPushButton, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QTextCursor

class CodeBlock(QFrame):
    """Widget for displaying code blocks with copy button."""
    
    def __init__(self, code: str, language: str = "", parent=None):
        super().__init__(parent)
        self.code = code
        self.language = language
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #0d1117;
                border-radius: 6px;
                border: 1px solid #30363d;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #161b22; border-top-left-radius: 6px; border-top-right-radius: 6px; border-bottom: 1px solid #30363d;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        lang_label = QLabel(self.language or "text")
        lang_label.setStyleSheet("color: #8b949e; font-family: 'Segoe UI', sans-serif; font-size: 12px; font-weight: bold; border: none;")
        header_layout.addWidget(lang_label)
        
        header_layout.addStretch()
        
        copy_btn = QPushButton("Copy")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8b949e;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #58a6ff;
            }
        """)
        copy_btn.clicked.connect(self.copy_code)
        header_layout.addWidget(copy_btn)
        
        layout.addWidget(header)
        
        # Code Content
        content = QTextBrowser()
        content.setPlainText(self.code)
        content.setReadOnly(True)
        content.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                color: #c9d1d9;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                border: none;
                padding: 10px;
            }
        """)
        content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Adjust height to fit content
        doc_height = content.document().size().height()
        content.setFixedHeight(int(doc_height + 20))
        
        layout.addWidget(content)
        
    def copy_code(self):
        pyperclip.copy(self.code)
        # Optional: Feedback (Change button text temporarily)

class MessageBubble(QFrame):
    """A chat message bubble widget."""
    
    def __init__(self, message: str, is_user: bool = False, sender_name: str = "", parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.sender_name = sender_name
        self.full_text = message
        self.setup_ui()
        self.render_content(message)
    
    def setup_ui(self):
        """Initialize the UI layout."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)
        
        if self.is_user:
            self.setObjectName("chatBubbleUser")
        else:
            self.setObjectName("chatBubbleAI")
            
        if self.sender_name:
            name_label = QLabel(self.sender_name)
            name_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            name_label.setStyleSheet("color: #e94560;" if not self.is_user else "color: #ffffff; border: none;")
            self.layout.addWidget(name_label)
            
        self.content_container = QVBoxLayout()
        self.content_container.setSpacing(10)
        self.layout.addLayout(self.content_container)
        
        self.setMaximumWidth(800)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

    def render_content(self, text: str):
        """Parse and render content (text/markdown/code)."""
        # Clear existing content
        while self.content_container.count():
            item = self.content_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Simple parser for code blocks
        parts = []
        last_end = 0
        pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
        
        for match in pattern.finditer(text):
            start, end = match.span()
            if start > last_end:
                parts.append({"type": "text", "content": text[last_end:start]})
            
            lang = match.group(1) or "text"
            code = match.group(2)
            parts.append({"type": "code", "language": lang, "content": code})
            last_end = end
            
        if last_end < len(text):
            parts.append({"type": "text", "content": text[last_end:]})
            
        for part in parts:
            if part["type"] == "code":
                code_block = CodeBlock(part["content"], part["language"])
                self.content_container.addWidget(code_block)
            else:
                # Render Markdown
                html = markdown.markdown(part["content"], extensions=['fenced_code', 'nl2br'])
                browser = QTextBrowser()
                browser.setHtml(html)
                browser.setOpenExternalLinks(True)
                browser.setStyleSheet("background-color: transparent; border: none; color: " + ("white" if self.is_user else "#eaeaea") + ";")
                browser.setFont(QFont("Segoe UI", 11))
                
                # Auto-resize height
                doc = browser.document()
                doc.setTextWidth(self.width() - 40) # Approximate width
                height = doc.size().height()
                browser.setFixedHeight(int(height + 20))
                
                self.content_container.addWidget(browser)

    def update_text(self, text: str):
        """Update text (optimized for streaming - currently just re-renders)."""
        # For true fade-in streaming, we would need to append to the last text widget.
        # But switching to complex rendering makes that hard.
        # We will just re-render for now, but maybe optimize if only appending text.
        self.full_text = text
        self.render_content(text)

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
        
        # Add opacity effect for fade-in
        opacity_effect = QGraphicsOpacityEffect(bubble)
        bubble.setGraphicsEffect(opacity_effect)
        
        anim = QPropertyAnimation(opacity_effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
        
        # Keep reference to animation to prevent GC
        bubble.anim = anim
        
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, container)
        self.messages.append({"role": "user" if is_user else "assistant", "content": message})
        
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def update_last_message(self, content: str):
        """Update the content of the last message (for streaming)."""
        if self.messages_layout.count() > 1:
            last_container = self.messages_layout.itemAt(self.messages_layout.count() - 2).widget()
            if last_container:
                bubble = last_container.findChild(MessageBubble)
                if bubble:
                    bubble.update_text(content)
        
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

from PyQt5.QtWidgets import QGraphicsOpacityEffect
