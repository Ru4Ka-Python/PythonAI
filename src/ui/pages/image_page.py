"""Image Generator page."""

import os
import requests
from datetime import datetime

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QComboBox, QGroupBox, QFrame, QScrollArea,
    QGridLayout, QFileDialog, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QPixmap, QImage

from .base_page import BasePage
from ...config import AVAILABLE_IMAGE_SIZES


class ImageGeneratorWorker(QThread):
    """Worker thread for image generation."""
    
    image_generated = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, client, prompt, model, size, quality):
        super().__init__()
        self.client = client
        self.prompt = prompt
        self.model = model
        self.size = size
        self.quality = quality
    
    def run(self):
        """Generate the image."""
        try:
            urls = self.client.generate_image(
                prompt=self.prompt,
                model=self.model,
                size=self.size,
                quality=self.quality
            )
            if urls:
                self.image_generated.emit(urls[0], self.prompt)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ImageCard(QFrame):
    """Widget for displaying a generated image."""
    
    def __init__(self, image_url: str, prompt: str, parent=None):
        super().__init__(parent)
        self.image_url = image_url
        self.prompt = prompt
        self.pixmap = None
        self.setup_ui()
        self.load_image()
    
    def setup_ui(self):
        """Initialize the UI."""
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        self.setFixedSize(300, 350)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.image_label = QLabel("Loading...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(280, 280)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #0f3460;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.image_label)
        
        self.prompt_label = QLabel(self.prompt[:50] + "..." if len(self.prompt) > 50 else self.prompt)
        self.prompt_label.setWordWrap(True)
        self.prompt_label.setStyleSheet("color: #8a8a8a; font-size: 11px;")
        self.prompt_label.setToolTip(self.prompt)
        layout.addWidget(self.prompt_label)
    
    def load_image(self):
        """Load image from URL."""
        try:
            response = requests.get(self.image_url, timeout=30)
            if response.status_code == 200:
                image = QImage()
                image.loadFromData(response.content)
                self.pixmap = QPixmap.fromImage(image)
                scaled = self.pixmap.scaled(
                    280, 280,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)
        except Exception as e:
            self.image_label.setText(f"Failed to load:\n{str(e)[:50]}")
    
    def save_image(self, path: str):
        """Save image to file."""
        if self.pixmap:
            self.pixmap.save(path)


class ImageGeneratorPage(BasePage):
    """Page for generating images."""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Image Generator",
            subtitle="Generate images using DALL-E AI",
            parent=parent
        )
        self.image_worker = None
        self.generated_images = []
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = self.create_header()
        layout.addLayout(header)
        
        input_group = QGroupBox("Image Description")
        input_layout = QVBoxLayout(input_group)
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
            "Describe the image you want to generate...\n"
            "Example: A serene mountain landscape at sunset with vibrant orange and purple colors"
        )
        self.prompt_input.setMaximumHeight(100)
        input_layout.addWidget(self.prompt_input)
        
        layout.addWidget(input_group)
        
        options_layout = QHBoxLayout()
        options_layout.setSpacing(20)
        
        size_group = QGroupBox("Image Size")
        size_layout = QVBoxLayout(size_group)
        self.size_combo = QComboBox()
        self.size_combo.addItems(AVAILABLE_IMAGE_SIZES)
        size_layout.addWidget(self.size_combo)
        options_layout.addWidget(size_group)
        
        quality_group = QGroupBox("Quality")
        quality_layout = QVBoxLayout(quality_group)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["standard", "hd"])
        quality_layout.addWidget(self.quality_combo)
        options_layout.addWidget(quality_group)
        
        options_layout.addStretch()
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.generate_button = QPushButton("Generate Image")
        self.generate_button.setObjectName("primaryButton")
        self.generate_button.setCursor(Qt.PointingHandCursor)
        self.generate_button.clicked.connect(self.generate_image)
        button_layout.addWidget(self.generate_button)
        
        self.save_button = QPushButton("Save Selected")
        self.save_button.setObjectName("secondaryButton")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_selected_image)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)
        
        options_layout.addLayout(button_layout)
        layout.addLayout(options_layout)
        
        gallery_label = QLabel("Generated Images")
        gallery_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(gallery_label)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_widget)
        self.gallery_layout.setSpacing(20)
        self.gallery_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.scroll_area.setWidget(self.gallery_widget)
        layout.addWidget(self.scroll_area, 1)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        layout.addWidget(self.status_label)
    
    def generate_image(self):
        """Generate a new image."""
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.show_warning("Warning", "Please enter an image description.")
            return
        
        if not self._openai_client or not self._openai_client.is_configured():
            self.show_error("Error", "Please configure your OpenAI API key in Settings.")
            return
        
        self.generate_button.setEnabled(False)
        self.status_label.setText("Generating image... This may take a moment.")
        
        self.image_worker = ImageGeneratorWorker(
            client=self._openai_client,
            prompt=prompt,
            model=self.config.image_model,
            size=self.size_combo.currentText(),
            quality=self.quality_combo.currentText()
        )
        self.image_worker.image_generated.connect(self.on_image_generated)
        self.image_worker.error_occurred.connect(self.on_error)
        self.image_worker.start()
    
    def on_image_generated(self, url: str, prompt: str):
        """Handle generated image."""
        self.generate_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.status_label.setText("Image generated successfully!")
        
        card = ImageCard(url, prompt)
        self.generated_images.append(card)
        
        row = (len(self.generated_images) - 1) // 3
        col = (len(self.generated_images) - 1) % 3
        self.gallery_layout.addWidget(card, row, col)
    
    def on_error(self, error_message: str):
        """Handle errors."""
        self.generate_button.setEnabled(True)
        self.status_label.setText("")
        self.show_error("Error", f"Failed to generate image: {error_message}")
    
    def save_selected_image(self):
        """Save the most recent image."""
        if not self.generated_images:
            return
        
        latest_card = self.generated_images[-1]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"generated_image_{timestamp}.png"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            default_name,
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
        )
        
        if file_path:
            latest_card.save_image(file_path)
            self.show_info("Success", f"Image saved to: {file_path}")
