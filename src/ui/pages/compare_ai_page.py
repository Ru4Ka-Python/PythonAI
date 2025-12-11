"""Compare AI Page."""

import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTextEdit, QComboBox, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from .base_page import BasePage
from ..widgets.chat_widget import ChatWidget
from ...api.llm_client import LLMClient

class CompareWorker(QThread):
    """Worker thread for running comparisons."""
    chunk_received = pyqtSignal(int, str)  # index (0 or 1), content
    finished = pyqtSignal(int, float, int) # index, duration, token_count (approx)
    error = pyqtSignal(int, str)

    def __init__(self, client, message, config1, config2):
        super().__init__()
        self.client = client
        self.message = message
        self.config1 = config1
        self.config2 = config2
        
    def run(self):
        # We need to run two requests. Since this is a single thread, we'll do them sequentially or use sub-threads?
        # Ideally parallel. But for simplicity in this worker, let's do sequential or simple async.
        # But user wants to see them generate. Sequential is bad UX.
        # So this worker should manage two other threads or use asyncio.
        # Given PyQt constraints, let's spawn two separate workers from the page instead.
        pass

class SingleModelWorker(QThread):
    """Worker for a single model."""
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(float, int)
    error = pyqtSignal(str)
    
    def __init__(self, client, message, model, provider, temperature, max_tokens):
        super().__init__()
        self.client = client
        self.message = [{"role": "user", "content": message}]
        self.model = model
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def run(self):
        start_time = time.time()
        token_count = 0
        try:
            for chunk in self.client.chat_stream(
                messages=self.message,
                model=self.model,
                provider=self.provider,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            ):
                self.chunk_received.emit(chunk)
                token_count += 1 # Very rough approximation
                
            duration = time.time() - start_time
            self.finished.emit(duration, token_count)
            
        except Exception as e:
            self.error.emit(str(e))

class CompareAIPage(BasePage):
    """Page for comparing two AI models."""
    
    def __init__(self, parent=None):
        super().__init__("Compare AI", "Compare performance and responses of different models", parent)
        self.llm_client = None
        self.workers = [None, None]
        self.current_history_id = None
        self.setup_ui()
        
    def set_llm_client(self, client):
        self.llm_client = client
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        layout.addLayout(self.create_header())
        
        # Models Selection
        sel_layout = QHBoxLayout()
        
        # Model 1
        self.model1_provider = QComboBox()
        self.model1_provider.addItems(["openai", "gemini"])
        self.model1_model = QComboBox() # Populate based on provider
        
        # Model 2
        self.model2_provider = QComboBox()
        self.model2_provider.addItems(["openai", "gemini"])
        self.model2_model = QComboBox()

        sel_layout.addWidget(QLabel("Model 1:"))
        sel_layout.addWidget(self.model1_provider)
        sel_layout.addWidget(self.model1_model)
        sel_layout.addStretch()
        sel_layout.addWidget(QLabel("Model 2:"))
        sel_layout.addWidget(self.model2_provider)
        sel_layout.addWidget(self.model2_model)
        
        layout.addLayout(sel_layout)
        
        self.model1_provider.currentTextChanged.connect(lambda t: self.update_models(1, t))
        self.model2_provider.currentTextChanged.connect(lambda t: self.update_models(2, t))
        
        # Initial population
        self.update_models(1, "openai")
        self.update_models(2, "openai") # Default to openai for both initially
        
        # Splitter for Chats
        splitter = QSplitter(Qt.Horizontal)
        
        # Chat 1 Container
        c1_widget = QWidget()
        c1_layout = QVBoxLayout(c1_widget)
        self.chat1 = ChatWidget()
        self.stats1 = QLabel("Speed: - | Tokens: -")
        c1_layout.addWidget(self.chat1)
        c1_layout.addWidget(self.stats1)
        
        # Chat 2 Container
        c2_widget = QWidget()
        c2_layout = QVBoxLayout(c2_widget)
        self.chat2 = ChatWidget()
        self.stats2 = QLabel("Speed: - | Tokens: -")
        c2_layout.addWidget(self.chat2)
        c2_layout.addWidget(self.stats2)
        
        splitter.addWidget(c1_widget)
        splitter.addWidget(c2_widget)
        
        layout.addWidget(splitter, 1)
        
        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type your message here to send to both models...")
        self.input_field.setMaximumHeight(80)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("primaryButton")
        self.send_btn.clicked.connect(self.start_comparison)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
    def update_models(self, index, provider):
        combo = self.model1_model if index == 1 else self.model2_model
        combo.clear()
        if provider == "openai":
            combo.addItems(["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"])
        else:
            combo.addItems(["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"])
            
    def start_comparison(self):
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        
        self.chat1.add_message(message, is_user=True)
        self.chat2.add_message(message, is_user=True)
        
        self.input_field.clear()
        
        # Start Workers
        self.start_worker(0, message, self.model1_provider.currentText(), self.model1_model.currentText())
        self.start_worker(1, message, self.model2_provider.currentText(), self.model2_model.currentText())
        
    def start_worker(self, index, message, provider, model):
        if not self.llm_client:
            chat_widget = self.chat1 if index == 0 else self.chat2
            chat_widget.add_message("Connection error: LLM Client not initialized", is_user=False, sender_name=f"{model} ({provider})")
            return
        
        try:
            worker = SingleModelWorker(
                self.llm_client, message, model, provider, 
                self.config.temperature, self.config.max_tokens
            )
            
            chat_widget = self.chat1 if index == 0 else self.chat2
            stats_label = self.stats1 if index == 0 else self.stats2
            
            # Add initial AI message
            chat_widget.add_message("", is_user=False, sender_name=f"{model} ({provider})")
            
            worker.chunk_received.connect(lambda c: chat_widget.update_last_message(
                chat_widget.get_messages()[-1]["content"] + c
            ))
            
            worker.finished.connect(lambda d, t: self.update_stats(index, d, t))
            worker.error.connect(lambda e: self.on_worker_error(index, e))
            
            # Clean up existing worker if any
            if self.workers[index] and self.workers[index].isRunning():
                self.workers[index].terminate()
                
            self.workers[index] = worker
            worker.start()
        except Exception as e:
            chat_widget = self.chat1 if index == 0 else self.chat2
            chat_widget.add_message(f"Error: {str(e)}", is_user=False, sender_name=f"{model} ({provider})")
    
    def on_worker_error(self, index, error_message):
        """Handle worker error."""
        chat_widget = self.chat1 if index == 0 else self.chat2
        if chat_widget.get_messages() and not chat_widget.get_messages()[-1]["content"]:
            chat_widget.update_last_message(f"Connection error: {error_message}")
        else:
            chat_widget.add_message(f"Connection error: {error_message}", is_user=False)
        
    def update_stats(self, index, duration, tokens):
        label = self.stats1 if index == 0 else self.stats2
        speed = tokens / duration if duration > 0 else 0
        label.setText(f"Time: {duration:.2f}s | Speed: {speed:.2f} tok/s")
        self.save_history()
    
    def load_history_item(self, item):
        """Load comparison history."""
        self.current_history_id = item['id']
        data = item['data']
        
        messages1 = data.get('messages1', [])
        messages2 = data.get('messages2', [])
        
        self.chat1.clear_messages()
        self.chat2.clear_messages()
        
        for msg in messages1:
            is_user = msg["role"] == "user"
            self.chat1.add_message(msg["content"], is_user=is_user, sender_name="You" if is_user else "AI")
        
        for msg in messages2:
            is_user = msg["role"] == "user"
            self.chat2.add_message(msg["content"], is_user=is_user, sender_name="You" if is_user else "AI")
    
    def load_history_data(self, data):
        """Load comparison history (compatibility method)."""
        self.load_history_item({"id": None, "data": data})
    
    def save_history(self):
        """Save comparison to history."""
        if not self._history_manager:
            return
        
        messages1 = self.chat1.get_messages()
        messages2 = self.chat2.get_messages()
        
        data = {
            "messages1": messages1,
            "messages2": messages2,
            "model1": {
                "provider": self.model1_provider.currentText(),
                "model": self.model1_model.currentText()
            },
            "model2": {
                "provider": self.model2_provider.currentText(),
                "model": self.model2_model.currentText()
            }
        }
        
        if self.current_history_id:
            self._history_manager.update_item_data("compare_ai", self.current_history_id, data)
        else:
            title = "Comparison"
            if messages1:
                first_msg = messages1[0]['content']
                title = (first_msg[:30] + '...') if len(first_msg) > 30 else first_msg
            
            item = self._history_manager.add_item("compare_ai", title, data)
            self.current_history_id = item['id']

