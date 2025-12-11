"""Settings page."""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QGroupBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QCheckBox, QScrollArea,
    QWidget, QFormLayout, QFontComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .base_page import BasePage
from ...config import AVAILABLE_MODELS


class SettingsPage(BasePage):
    """Page for application settings."""
    
    settings_changed = pyqtSignal()
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(
            title="Settings",
            subtitle="Configure your API keys and preferences",
            parent=parent
        )
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        header = self.create_header()
        main_layout.addLayout(header)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setSpacing(20)
        
        # API Keys
        api_group = QGroupBox("API Keys")
        api_layout = QFormLayout(api_group)
        api_layout.setSpacing(15)
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("sk-...")
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("OpenAI API Key:", self.openai_key_input)
        
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setPlaceholderText("Gemini API key")
        self.gemini_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("Gemini API Key:", self.gemini_key_input)
        
        self.lumaai_key_input = QLineEdit()
        self.lumaai_key_input.setPlaceholderText("LumaAI API key")
        self.lumaai_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("LumaAI API Key:", self.lumaai_key_input)
        
        layout.addWidget(api_group)
        
        # Model Settings
        model_group = QGroupBox("AI Model Settings")
        model_layout = QFormLayout(model_group)
        model_layout.setSpacing(15)
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["openai", "gemini"])
        self.provider_combo.currentTextChanged.connect(self.update_model_list)
        model_layout.addRow("Model Type:", self.provider_combo)
        
        self.model_combo = QComboBox()
        # Initial population handled by update_model_list
        model_layout.addRow("Chat Model:", self.model_combo)
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 32000)
        self.max_tokens_spin.setValue(2048)
        self.max_tokens_spin.setSingleStep(100)
        model_layout.addRow("Max Tokens:", self.max_tokens_spin)
        
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setDecimals(1)
        model_layout.addRow("Temperature:", self.temperature_spin)
        
        layout.addWidget(model_group)
        
        # System Prompts
        prompt_group = QGroupBox("System Prompts")
        prompt_layout = QVBoxLayout(prompt_group)
        prompt_layout.setSpacing(15)
        
        chat_prompt_label = QLabel("Chat System Prompt:")
        prompt_layout.addWidget(chat_prompt_label)
        
        self.system_prompt_input = QTextEdit()
        self.system_prompt_input.setPlaceholderText("Enter the system prompt for chat mode...")
        self.system_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.system_prompt_input)
        
        ai1_label = QLabel("AI-1 Name & System Prompt:")
        prompt_layout.addWidget(ai1_label)
        
        self.ai1_name_input = QLineEdit()
        self.ai1_name_input.setPlaceholderText("Name for AI-1")
        prompt_layout.addWidget(self.ai1_name_input)
        
        self.ai1_prompt_input = QTextEdit()
        self.ai1_prompt_input.setPlaceholderText("Enter the system prompt for AI-1...")
        self.ai1_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.ai1_prompt_input)
        
        ai2_label = QLabel("AI-2 Name & System Prompt:")
        prompt_layout.addWidget(ai2_label)
        
        self.ai2_name_input = QLineEdit()
        self.ai2_name_input.setPlaceholderText("Name for AI-2")
        prompt_layout.addWidget(self.ai2_name_input)
        
        self.ai2_prompt_input = QTextEdit()
        self.ai2_prompt_input.setPlaceholderText("Enter the system prompt for AI-2...")
        self.ai2_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.ai2_prompt_input)
        
        layout.addWidget(prompt_group)
        
        # Appearance
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(appearance_group)
        appearance_layout.setSpacing(15)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        appearance_layout.addRow("Theme:", self.theme_combo)
        
        self.font_combo = QFontComboBox()
        self.font_combo.setFontFilters(QFontComboBox.ScalableFonts)
        appearance_layout.addRow("System Font:", self.font_combo)
        
        layout.addWidget(appearance_group)
        
        # Misc
        misc_group = QGroupBox("Miscellaneous")
        misc_layout = QVBoxLayout(misc_group)
        
        self.auto_update_check = QCheckBox("Automatically check for updates on startup")
        misc_layout.addWidget(self.auto_update_check)
        
        layout.addWidget(misc_group)
        
        layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.save_button = QPushButton("Save Settings")
        self.save_button.setObjectName("primaryButton")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setObjectName("secondaryButton")
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #8a8a8a;")
        main_layout.addWidget(self.status_label)
        
        self.update_model_list("openai")
    
    def update_model_list(self, provider):
        """Update available models based on provider."""
        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        
        if provider == "openai":
            self.model_combo.addItems(["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"])
        elif provider == "gemini":
            self.model_combo.addItems(["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"])
            
    def load_settings(self):
        """Load current settings into the UI."""
        if not self.config:
            return
        
        self.openai_key_input.setText(self.config.openai_api_key)
        self.gemini_key_input.setText(self.config.gemini_api_key)
        self.lumaai_key_input.setText(self.config.lumaai_api_key)
        
        # Set provider first
        index = self.provider_combo.findText(self.config.chat_model_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        
        # Update model list and select model
        self.update_model_list(self.config.chat_model_provider)
        
        target_model = self.config.openai_model if self.config.chat_model_provider == "openai" else self.config.gemini_model
        index = self.model_combo.findText(target_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        self.max_tokens_spin.setValue(self.config.max_tokens)
        self.temperature_spin.setValue(self.config.temperature)
        
        self.system_prompt_input.setPlainText(self.config.system_prompt)
        self.ai1_prompt_input.setPlainText(self.config.ai1_system_prompt)
        self.ai2_prompt_input.setPlainText(self.config.ai2_system_prompt)
        self.ai1_name_input.setText(self.config.ai1_name)
        self.ai2_name_input.setText(self.config.ai2_name)
        
        index = self.theme_combo.findText(self.config.theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            
        font = QFont(self.config.font_family)
        self.font_combo.setCurrentFont(font)
        
        self.auto_update_check.setChecked(self.config.auto_check_updates)
    
    def save_settings(self):
        """Save settings to configuration."""
        if not self._config_manager:
            return
            
        provider = self.provider_combo.currentText()
        model = self.model_combo.currentText()
        
        openai_model = model if provider == "openai" else self.config.openai_model
        gemini_model = model if provider == "gemini" else self.config.gemini_model
        
        self._config_manager.update(
            openai_api_key=self.openai_key_input.text().strip(),
            gemini_api_key=self.gemini_key_input.text().strip(),
            lumaai_api_key=self.lumaai_key_input.text().strip(),
            chat_model_provider=provider,
            openai_model=openai_model,
            gemini_model=gemini_model,
            max_tokens=self.max_tokens_spin.value(),
            temperature=self.temperature_spin.value(),
            system_prompt=self.system_prompt_input.toPlainText().strip(),
            ai1_system_prompt=self.ai1_prompt_input.toPlainText().strip(),
            ai2_system_prompt=self.ai2_prompt_input.toPlainText().strip(),
            ai1_name=self.ai1_name_input.text().strip(),
            ai2_name=self.ai2_name_input.text().strip(),
            theme=self.theme_combo.currentText(),
            font_family=self.font_combo.currentFont().family(),
            auto_check_updates=self.auto_update_check.isChecked()
        )
        
        self.settings_changed.emit()
        self.status_label.setText("Settings saved successfully!")
        self.show_info("Success", "Settings have been saved.")
    
    def reset_settings(self):
        """Reset settings to defaults."""
        from ..config import AppConfig
        
        defaults = AppConfig()
        
        self.openai_key_input.clear()
        self.gemini_key_input.clear()
        self.lumaai_key_input.clear()
        
        # Reset provider/model
        index = self.provider_combo.findText("openai")
        if index >= 0: self.provider_combo.setCurrentIndex(index)
        
        self.update_model_list("openai")
        index = self.model_combo.findText(defaults.openai_model)
        if index >= 0: self.model_combo.setCurrentIndex(index)
        
        self.max_tokens_spin.setValue(defaults.max_tokens)
        self.temperature_spin.setValue(defaults.temperature)
        
        self.system_prompt_input.setPlainText(defaults.system_prompt)
        self.ai1_prompt_input.setPlainText(defaults.ai1_system_prompt)
        self.ai2_prompt_input.setPlainText(defaults.ai2_system_prompt)
        self.ai1_name_input.setText(defaults.ai1_name)
        self.ai2_name_input.setText(defaults.ai2_name)
        
        index = self.theme_combo.findText(defaults.theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            
        self.font_combo.setCurrentFont(QFont("Segoe UI"))
        
        self.auto_update_check.setChecked(defaults.auto_check_updates)
        
        self.status_label.setText("Settings reset to defaults (not saved yet)")
    
    def on_theme_changed(self, theme: str):
        """Handle theme change."""
        self.theme_changed.emit(theme)
