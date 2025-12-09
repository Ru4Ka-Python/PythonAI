"""Video Generator page."""

import os
import requests
import webbrowser
from datetime import datetime

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QComboBox, QGroupBox, QProgressBar,
    QCheckBox, QListWidget, QListWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

from .base_page import BasePage


class VideoGeneratorWorker(QThread):
    """Worker thread for video generation."""
    
    status_update = pyqtSignal(str, str)
    video_ready = pyqtSignal(str, str, str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, client, prompt, aspect_ratio, loop):
        super().__init__()
        self.client = client
        self.prompt = prompt
        self.aspect_ratio = aspect_ratio
        self.loop = loop
    
    def run(self):
        """Generate the video."""
        try:
            result = self.client.generate_video(
                prompt=self.prompt,
                aspect_ratio=self.aspect_ratio,
                loop=self.loop
            )
            
            if result.status.value == "failed":
                self.error_occurred.emit(result.error or "Unknown error")
                return
            
            generation_id = result.id
            self.status_update.emit(generation_id, "Video generation started...")
            
            final_result = self.client.wait_for_completion(
                generation_id=generation_id,
                timeout=600,
                poll_interval=10,
                callback=lambda r: self.status_update.emit(
                    generation_id,
                    f"Status: {r.status.value}"
                )
            )
            
            if final_result.status.value == "completed" and final_result.url:
                self.video_ready.emit(generation_id, final_result.url, self.prompt)
            else:
                self.error_occurred.emit(final_result.error or "Video generation failed")
                
        except Exception as e:
            self.error_occurred.emit(str(e))


class VideoItem(QListWidgetItem):
    """List item representing a generated video."""
    
    def __init__(self, generation_id: str, prompt: str, url: str = ""):
        super().__init__()
        self.generation_id = generation_id
        self.prompt = prompt
        self.url = url
        self.update_display("Generating...")
    
    def update_display(self, status: str):
        """Update the display text."""
        display_prompt = self.prompt[:50] + "..." if len(self.prompt) > 50 else self.prompt
        self.setText(f"🎬 {display_prompt}\n   Status: {status}")
    
    def set_ready(self, url: str):
        """Mark video as ready."""
        self.url = url
        self.update_display("Ready ✓")


class VideoGeneratorPage(BasePage):
    """Page for generating videos."""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Video Generator",
            subtitle="Generate videos using LumaAI",
            parent=parent
        )
        self.video_worker = None
        self.video_items = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        input_group = QGroupBox("Video Description")
        input_layout = QVBoxLayout(input_group)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Describe the video you want to generate...\n"
            "Example: A cinematic shot of a spaceship flying through a nebula"
        )
        self.prompt_input.setMaximumHeight(100)
        input_layout.addWidget(self.prompt_input)
        
        layout.addWidget(input_group)
        
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        aspect_group = QGroupBox("Aspect Ratio")
        aspect_layout = QVBoxLayout(aspect_group)
        self.aspect_combo = QComboBox()
        self.aspect_combo.addItems(["16:9", "9:16", "1:1", "4:3", "3:4"])
        aspect_layout.addWidget(self.aspect_combo)
        options_layout.addWidget(aspect_group)
        
        loop_group = QGroupBox("Options")
        loop_layout = QVBoxLayout(loop_group)
        self.loop_checkbox = QCheckBox("Loop video")
        loop_layout.addWidget(self.loop_checkbox)
        options_layout.addWidget(loop_group)
        
        options_layout.addStretch()
        
        self.generate_button = QPushButton("Generate Video")
        self.generate_button.setObjectName("primaryButton")
        self.generate_button.setCursor(Qt.PointingHandCursor)
        self.generate_button.clicked.connect(self.generate_video)
        options_layout.addWidget(self.generate_button)
        
        layout.addLayout(options_layout)
        
        videos_label = QLabel("Generated Videos")
        videos_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(videos_label)
        
        self.video_list = QListWidget()
        self.video_list.setStyleSheet("""
            QListWidget {
                background-color: #16213e;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                background-color: #0f3460;
                border-radius: 6px;
                padding: 15px;
                margin: 5px;
                color: #eaeaea;
            }
            QListWidget::item:selected {
                background-color: #e94560;
            }
        """)
        layout.addWidget(self.video_list, 1)
        
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        self.open_button = QPushButton("Open in Browser")
        self.open_button.setObjectName("secondaryButton")
        self.open_button.setCursor(Qt.PointingHandCursor)
        self.open_button.clicked.connect(self.open_video)
        self.open_button.setEnabled(False)
        action_layout.addWidget(self.open_button)
        
        self.download_button = QPushButton("Download Video")
        self.download_button.setObjectName("secondaryButton")
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.download_video)
        self.download_button.setEnabled(False)
        action_layout.addWidget(self.download_button)
        
        action_layout.addStretch()
        layout.addLayout(action_layout)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        layout.addWidget(self.status_label)
        
        self.video_list.itemSelectionChanged.connect(self.on_selection_changed)
    
    def generate_video(self):
        """Generate a new video."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.show_warning("Warning", "Please enter a video description.")
            return
        
        if not self._lumaai_client or not self._lumaai_client.is_configured():
            self.show_error("Error", "Please configure your LumaAI API key in Settings.")
            return
        
        self.generate_button.setEnabled(False)
        self.status_label.setText("Starting video generation...")
        
        self.video_worker = VideoGeneratorWorker(
            client=self._lumaai_client,
            prompt=prompt,
            aspect_ratio=self.aspect_combo.currentText(),
            loop=self.loop_checkbox.isChecked()
        )
        self.video_worker.status_update.connect(self.on_status_update)
        self.video_worker.video_ready.connect(self.on_video_ready)
        self.video_worker.error_occurred.connect(self.on_error)
        self.video_worker.start()
        
        temp_item = VideoItem("pending", prompt)
        self.video_list.addItem(temp_item)
    
    def on_status_update(self, generation_id: str, status: str):
        """Handle status updates."""
        self.status_label.setText(status)
        
        for i in range(self.video_list.count()):
            item = self.video_list.item(i)
            if isinstance(item, VideoItem):
                if item.generation_id == "pending":
                    item.generation_id = generation_id
                    self.video_items[generation_id] = item
                if item.generation_id == generation_id:
                    item.update_display(status)
    
    def on_video_ready(self, generation_id: str, url: str, prompt: str):
        """Handle video ready."""
        self.generate_button.setEnabled(True)
        self.status_label.setText("Video generated successfully!")
        
        if generation_id in self.video_items:
            self.video_items[generation_id].set_ready(url)
        
        self.on_selection_changed()
    
    def on_error(self, error_message: str):
        """Handle errors."""
        self.generate_button.setEnabled(True)
        self.status_label.setText("")
        self.show_error("Error", f"Failed to generate video: {error_message}")
    
    def on_selection_changed(self):
        """Handle selection change."""
        current_item = self.video_list.currentItem()
        if isinstance(current_item, VideoItem) and current_item.url:
            self.open_button.setEnabled(True)
            self.download_button.setEnabled(True)
        else:
            self.open_button.setEnabled(False)
            self.download_button.setEnabled(False)
    
    def open_video(self):
        """Open selected video in browser."""
        current_item = self.video_list.currentItem()
        if isinstance(current_item, VideoItem) and current_item.url:
            webbrowser.open(current_item.url)
    
    def download_video(self):
        """Download selected video."""
        current_item = self.video_list.currentItem()
        if not isinstance(current_item, VideoItem) or not current_item.url:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"generated_video_{timestamp}.mp4"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video",
            default_name,
            "MP4 Videos (*.mp4);;All Files (*)"
        )
        
        if file_path:
            try:
                self.status_label.setText("Downloading video...")
                response = requests.get(current_item.url, timeout=120)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                self.show_info("Success", f"Video saved to: {file_path}")
                self.status_label.setText("Video downloaded successfully!")
            except Exception as e:
                self.show_error("Error", f"Failed to download video: {str(e)}")
                self.status_label.setText("")
