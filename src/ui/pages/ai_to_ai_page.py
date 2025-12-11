"""AI-to-AI conversation page."""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .base_page import BasePage
from ..widgets.chat_widget import ChatWidget


class AIConversationWorker(QThread):
    """Worker thread for AI-to-AI conversation."""
    
    message_received = pyqtSignal(str, str, bool)
    error_occurred = pyqtSignal(str)
    conversation_ended = pyqtSignal()
    
    def __init__(self, client, ai1_prompt, ai2_prompt, ai1_name, ai2_name, topic, model, provider, max_tokens, temperature, turns):
        super().__init__()
        self.client = client
        self.ai1_prompt = ai1_prompt
        self.ai2_prompt = ai2_prompt
        self.ai1_name = ai1_name
        self.ai2_name = ai2_name
        self.topic = topic
        self.model = model
        self.provider = provider
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.turns = turns
        self.is_running = True
    
    def stop(self):
        """Stop the conversation."""
        self.is_running = False
    
    def run(self):
        """Execute the AI-to-AI conversation."""
        try:
            # We use non-streaming for AI-to-AI to keep turns clean, or we could stream.
            # For simplicity, using non-streaming chat wrapper if available, or just consume stream.
            
            # Since LLMClient only exposes chat_stream, we consume it.
            
            ai1_history = [
                {"role": "system", "content": self.ai1_prompt},
                {"role": "user", "content": f"Start a conversation about: {self.topic}"}
            ]
            ai2_history = [
                {"role": "system", "content": self.ai2_prompt}
            ]
            
            for turn in range(self.turns):
                if not self.is_running:
                    break
                
                # AI 1 Turn
                ai1_response = ""
                for chunk in self.client.chat_stream(
                    messages=ai1_history,
                    model=self.model,
                    provider=self.provider,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ):
                    ai1_response += chunk
                
                if not self.is_running: break
                
                self.message_received.emit(self.ai1_name, ai1_response, False)
                ai1_history.append({"role": "assistant", "content": ai1_response})
                ai2_history.append({"role": "user", "content": ai1_response})
                
                # AI 2 Turn
                ai2_response = ""
                for chunk in self.client.chat_stream(
                    messages=ai2_history,
                    model=self.model,
                    provider=self.provider,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ):
                    ai2_response += chunk
                    
                if not self.is_running: break
                
                self.message_received.emit(self.ai2_name, ai2_response, True)
                ai2_history.append({"role": "assistant", "content": ai2_response})
                ai1_history.append({"role": "user", "content": ai2_response})
            
            self.conversation_ended.emit()
            
        except Exception as e:
            self.error_occurred.emit(str(e))


class AIToAIPage(BasePage):
    """Page for AI-to-AI conversations."""
    
    def __init__(self, parent=None):
        super().__init__(
            title="AI-to-AI Chat",
            subtitle="Watch two AI assistants have a conversation",
            parent=parent
        )
        self.conversation_worker = None
        self.messages = []
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        config_layout = QHBoxLayout()
        config_layout.setSpacing(20)
        
        topic_group = QGroupBox("Conversation Topic")
        topic_layout = QVBoxLayout(topic_group)
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter a topic for the AIs to discuss...")
        topic_layout.addWidget(self.topic_input)
        config_layout.addWidget(topic_group, 2)
        
        turns_group = QGroupBox("Number of Turns")
        turns_layout = QVBoxLayout(turns_group)
        self.turns_spinbox = QSpinBox()
        self.turns_spinbox.setRange(1, 20)
        self.turns_spinbox.setValue(5)
        turns_layout.addWidget(self.turns_spinbox)
        config_layout.addWidget(turns_group)
        
        layout.addLayout(config_layout)
        
        self.chat_widget = ChatWidget()
        layout.addWidget(self.chat_widget, 1)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.start_button = QPushButton("Start Conversation")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_conversation)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("secondaryButton")
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_conversation)
        button_layout.addWidget(self.stop_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        layout.addWidget(self.status_label)
    
    def load_history_data(self, data):
        """Load history."""
        self.messages = data.get("messages", [])
        self.topic_input.setText(data.get("topic", ""))
        self.chat_widget.clear_messages()
        
        for msg in self.messages:
            self.chat_widget.add_message(msg['content'], is_user=msg.get('is_ai2', False), sender_name=msg.get('sender', 'AI'))

    def start_conversation(self):
        """Start the AI-to-AI conversation."""
        topic = self.topic_input.text().strip()
        if not topic:
            self.show_warning("Warning", "Please enter a conversation topic.")
            return
        
        if not self._llm_client:
            self.show_error("Error", "LLM Client not initialized.")
            return
        
        self.clear_chat(False) # Clear widgets but keep input
        self.messages = [] # New history
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.topic_input.setEnabled(False)
        self.turns_spinbox.setEnabled(False)
        self.status_label.setText("Conversation in progress...")
        
        provider = self.config.chat_model_provider
        model = self.config.openai_model if provider == "openai" else self.config.gemini_model

        self.conversation_worker = AIConversationWorker(
            client=self._llm_client,
            ai1_prompt=self.config.ai1_system_prompt,
            ai2_prompt=self.config.ai2_system_prompt,
            ai1_name=self.config.ai1_name,
            ai2_name=self.config.ai2_name,
            topic=topic,
            model=model,
            provider=provider,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            turns=self.turns_spinbox.value()
        )
        self.conversation_worker.message_received.connect(self.on_message_received)
        self.conversation_worker.error_occurred.connect(self.on_error)
        self.conversation_worker.conversation_ended.connect(self.on_conversation_ended)
        self.conversation_worker.start()
        
        # Save initial state
        self.save_history()
    
    def stop_conversation(self):
        """Stop the ongoing conversation."""
        if self.conversation_worker:
            self.conversation_worker.stop()
        self.on_conversation_ended()
    
    def on_message_received(self, sender: str, message: str, is_ai2: bool):
        """Handle received messages."""
        self.chat_widget.add_message(message, is_user=is_ai2, sender_name=sender)
        self.messages.append({
            "sender": sender,
            "content": message,
            "is_ai2": is_ai2
        })
        self.save_history()
    
    def on_error(self, error_message: str):
        """Handle errors."""
        self.on_conversation_ended()
        self.show_error("Error", f"Conversation error: {error_message}")
    
    def on_conversation_ended(self):
        """Handle conversation end."""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.topic_input.setEnabled(True)
        self.turns_spinbox.setEnabled(True)
        self.status_label.setText("Conversation ended")
        self.save_history()
    
    def clear_chat(self, clear_history=True):
        """Clear the chat."""
        self.chat_widget.clear_messages()
        self.status_label.setText("")
        if clear_history:
            self.messages = []
            
    def save_history(self):
        if not self._history_manager: return
        
        data = {
            "topic": self.topic_input.text(),
            "messages": self.messages
        }
        
        # Determine title
        title = f"Topic: {self.topic_input.text()}"
        
        # This is simplified: Always adding new item for new conversation run is better than updating
        # But if we want to update the current running one...
        # We need an ID.
        if not hasattr(self, 'current_history_id') or self.current_history_id is None:
             item = self._history_manager.add_item("ai_to_ai", title, data)
             self.current_history_id = item['id']
        else:
             self._history_manager.update_item_data("ai_to_ai", self.current_history_id, data)
