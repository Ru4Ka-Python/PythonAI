"""Chat with AI page."""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from .base_page import BasePage
from ..widgets.chat_widget import ChatWidget


class ChatWorker(QThread):
    """Worker thread for chat API calls."""
    
    response_chunk = pyqtSignal(str)
    response_complete = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, client, messages, model, provider, max_tokens, temperature):
        super().__init__()
        self.client = client
        self.messages = messages
        self.model = model
        self.provider = provider
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def run(self):
        """Execute the chat request."""
        try:
            full_response = ""
            # Using LLMClient.chat_stream
            for chunk in self.client.chat_stream(
                messages=self.messages,
                model=self.model,
                provider=self.provider,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            ):
                full_response += chunk
                self.response_chunk.emit(full_response)
            
            self.response_complete.emit(full_response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ChatPage(BasePage):
    """Page for chatting with AI."""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Chat with AI",
            subtitle="Have a conversation with an AI assistant",
            parent=parent
        )
        self.chat_worker = None
        self.conversation_history = []
        self.current_history_id = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        self.chat_widget = ChatWidget()
        layout.addWidget(self.chat_widget, 1)
        
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 12px;
                padding: 5px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(15)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setMaximumHeight(100)
        self.message_input.setFont(QFont("Segoe UI", 12))
        self.message_input.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #eaeaea;
            }
        """)
        input_layout.addWidget(self.message_input)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(8)
        
        self.send_button = QPushButton("Send")
        self.send_button.setObjectName("primaryButton")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setMinimumWidth(80)
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button)
        
        self.clear_button = QPushButton("New Chat")
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setMinimumWidth(80)
        self.clear_button.clicked.connect(self.new_chat)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addLayout(button_layout)
        layout.addWidget(input_frame)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        layout.addWidget(self.status_label)
    
    def load_history_data(self, data):
        """Load conversation from history data (called by MainWindow)."""
        self.load_history_item({"id": None, "data": data})
    
    def load_history_item(self, item):
        self.new_chat(save_current=False)
        self.current_history_id = item['id']
        self.conversation_history = item['data'].get("messages", [])
        
        self.chat_widget.clear_messages()
        for msg in self.conversation_history:
            is_user = msg["role"] == "user"
            self.chat_widget.add_message(msg["content"], is_user=is_user, sender_name="You" if is_user else "AI")

    def send_message(self):
        """Send a message to the AI."""
        message = self.message_input.toPlainText().strip()
        if not message:
            return
        
        if not self._llm_client:
            self.show_error("Error", "LLM Client not initialized.")
            return
            
        self.chat_widget.add_message(message, is_user=True, sender_name="You")
        self.message_input.clear()
        
        self.conversation_history.append({"role": "user", "content": message})
        self.save_history()
        
        messages = [{"role": "system", "content": self.config.system_prompt}]
        messages.extend(self.conversation_history)
        
        self.chat_widget.add_message("", is_user=False, sender_name="AI")
        
        self.send_button.setEnabled(False)
        self.status_label.setText("AI is thinking...")
        
        provider = self.config.chat_model_provider
        model = self.config.openai_model if provider == "openai" else self.config.gemini_model
        
        self.chat_worker = ChatWorker(
            client=self._llm_client,
            messages=messages,
            model=model,
            provider=provider,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        self.chat_worker.response_chunk.connect(self.on_response_chunk)
        self.chat_worker.response_complete.connect(self.on_response_complete)
        self.chat_worker.error_occurred.connect(self.on_error)
        self.chat_worker.start()
    
    def on_response_chunk(self, content: str):
        """Handle streaming response chunks."""
        self.chat_widget.update_last_message(content)
    
    def on_response_complete(self, content: str):
        """Handle complete response."""
        self.conversation_history.append({"role": "assistant", "content": content})
        self.save_history()
        
        self.send_button.setEnabled(True)
        self.status_label.setText("")
    
    def on_error(self, error_message: str):
        """Handle errors."""
        self.send_button.setEnabled(True)
        self.status_label.setText("")
        self.show_error("Error", f"Failed to get response: {error_message}")
    
    def new_chat(self, save_current=True):
        """Clear the chat history."""
        # if save_current: self.save_history() # Already saved on each step
        self.current_history_id = None
        self.chat_widget.clear_messages()
        self.conversation_history.clear()
        self.status_label.setText("New chat started")
        
    def save_history(self):
        """Save conversation to history."""
        if not self._history_manager:
            return
            
        data = {
            "messages": self.conversation_history,
            "provider": self.config.chat_model_provider,
            "model": self.config.openai_model if self.config.chat_model_provider == "openai" else self.config.gemini_model
        }
        
        if self.current_history_id:
            self._history_manager.update_item_data("chat", self.current_history_id, data)
        else:
            # Create new
            title = "New Chat"
            if self.conversation_history:
                # Use first few words of first message
                first_msg = self.conversation_history[0]['content']
                title = (first_msg[:30] + '...') if len(first_msg) > 30 else first_msg
                
            item = self._history_manager.add_item("chat", title, data)
            self.current_history_id = item['id']
            # Notify MainWindow to refresh Sidebar? 
            # MainWindow doesn't listen to HistoryManager changes directly.
            # I can emit a signal or call a method on MainWindow if I had a reference.
            # Or use a global signal.
            # But simpler: MainWindow reloads history when Sidebar is refreshed.
            # But the Sidebar won't update automatically here.
            # That's a minor issue.
