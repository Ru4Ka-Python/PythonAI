"""Settings page."""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QGroupBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QCheckBox, QScrollArea,
    QWidget, QFormLayout
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
        
        api_group = QGroupBox("API Keys")
        api_layout = QFormLayout(api_group)
        api_layout.setSpacing(15)
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("sk-...")
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("OpenAI API Key:", self.openai_key_input)
        
        self.lumaai_key_input = QLineEdit()
        self.lumaai_key_input.setPlaceholderText("Your LumaAI API key")
        self.lumaai_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("LumaAI API Key:", self.lumaai_key_input)
        
        layout.addWidget(api_group)
        
        model_group = QGroupBox("AI Model Settings")
        model_layout = QFormLayout(model_group)
        model_layout.setSpacing(15)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(AVAILABLE_MODELS)
        model_layout.addRow("Chat Model:", self.model_combo)
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 8000)
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
        
        prompt_group = QGroupBox("System Prompts")
        prompt_layout = QVBoxLayout(prompt_group)
        prompt_layout.setSpacing(15)
        
        chat_prompt_label = QLabel("Chat System Prompt:")
        prompt_layout.addWidget(chat_prompt_label)
        
        self.system_prompt_input = QTextEdit()
        self.system_prompt_input.setPlaceholderText("Enter the system prompt for chat mode...")
        self.system_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.system_prompt_input)
        
        ai1_label = QLabel("AI-1 System Prompt:")
        prompt_layout.addWidget(ai1_label)
        
        self.ai1_prompt_input = QTextEdit()
        self.ai1_prompt_input.setPlaceholderText("Enter the system prompt for AI-1...")
        self.ai1_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.ai1_prompt_input)
        
        ai2_label = QLabel("AI-2 System Prompt:")
        prompt_layout.addWidget(ai2_label)
        
        self.ai2_prompt_input = QTextEdit()
        self.ai2_prompt_input.setPlaceholderText("Enter the system prompt for AI-2...")
        self.ai2_prompt_input.setMaximumHeight(80)
        prompt_layout.addWidget(self.ai2_prompt_input)
        
        layout.addWidget(prompt_group)
        
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout(appearance_group)
        appearance_layout.setSpacing(15)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        appearance_layout.addRow("Theme:", self.theme_combo)
        
        layout.addWidget(appearance_group)
        
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
    
    def load_settings(self):
        """Load current settings into the UI."""
        if not self.config:
            return
        
        self.openai_key_input.setText(self.config.openai_api_key)
        self.lumaai_key_input.setText(self.config.lumaai_api_key)
        
        index = self.model_combo.findText(self.config.openai_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        self.max_tokens_spin.setValue(self.config.max_tokens)
        self.temperature_spin.setValue(self.config.temperature)
        
        self.system_prompt_input.setPlainText(self.config.system_prompt)
        self.ai1_prompt_input.setPlainText(self.config.ai1_system_prompt)
        self.ai2_prompt_input.setPlainText(self.config.ai2_system_prompt)
        
        index = self.theme_combo.findText(self.config.theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        self.auto_update_check.setChecked(self.config.auto_check_updates)
    
    def save_settings(self):
        """Save settings to configuration."""
        if not self._config_manager:
            return
        
        self._config_manager.update(
            openai_api_key=self.openai_key_input.text().strip(),
            lumaai_api_key=self.lumaai_key_input.text().strip(),
            openai_model=self.model_combo.currentText(),
            max_tokens=self.max_tokens_spin.value(),
            temperature=self.temperature_spin.value(),
            system_prompt=self.system_prompt_input.toPlainText().strip(),
            ai1_system_prompt=self.ai1_prompt_input.toPlainText().strip(),
            ai2_system_prompt=self.ai2_prompt_input.toPlainText().strip(),
            theme=self.theme_combo.currentText(),
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
        self.lumaai_key_input.clear()
        
        index = self.model_combo.findText(defaults.openai_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        
        self.max_tokens_spin.setValue(defaults.max_tokens)
        self.temperature_spin.setValue(defaults.temperature)
        
        self.system_prompt_input.setPlainText(defaults.system_prompt)
        self.ai1_prompt_input.setPlainText(defaults.ai1_system_prompt)
        self.ai2_prompt_input.setPlainText(defaults.ai2_system_prompt)
        
        index = self.theme_combo.findText(defaults.theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        self.auto_update_check.setChecked(defaults.auto_check_updates)
        
        self.status_label.setText("Settings reset to defaults (not saved yet)")
    
    def on_theme_changed(self, theme: str):
        """Handle theme change."""
        self.theme_changed.emit(theme)
