"""Configuration management for RoleAI application."""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


CONFIG_FILE = "config.json"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_IMAGE_MODEL = "dall-e-3"
DEFAULT_IMAGE_SIZE = "1024x1024"
AVAILABLE_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
]
AVAILABLE_IMAGE_SIZES = ["1024x1024", "1024x1792", "1792x1024"]
GITHUB_REPO_URL = "https://api.github.com/repos/Ru4Ka-Python/PythonAI/releases/latest"
APP_VERSION = "1.6.0-beta"


@dataclass
class AppConfig:
    """Application configuration settings."""
    
    openai_api_key: str = ""
    gemini_api_key: str = ""
    lumaai_api_key: str = ""
    openai_model: str = DEFAULT_OPENAI_MODEL
    gemini_model: str = "gemini-2.0-flash"
    chat_model_provider: str = "openai"  # "openai" or "gemini"
    image_model: str = DEFAULT_IMAGE_MODEL
    image_size: str = DEFAULT_IMAGE_SIZE
    theme: str = "dark"
    font_family: str = "Segoe UI"
    auto_check_updates: bool = True
    max_tokens: int = 2048
    temperature: float = 0.7
    system_prompt: str = "You are a helpful AI assistant."
    ai1_name: str = "AI-1"
    ai2_name: str = "AI-2"
    ai1_system_prompt: str = "You are the first AI in a conversation. Be creative and engaging."
    ai2_system_prompt: str = "You are the second AI in a conversation. Respond thoughtfully."


class ConfigManager:
    """Manages application configuration persistence."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or CONFIG_FILE
        self.config = self.load()
    
    def load(self) -> AppConfig:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return AppConfig(**data)
            except (json.JSONDecodeError, TypeError):
                return AppConfig()
        return AppConfig()
    
    def save(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self.config), f, indent=2)
    
    def update(self, **kwargs) -> None:
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save()
