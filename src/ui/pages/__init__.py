"""Page widgets for RoleAI."""

from .chat_page import ChatPage
from .ai_to_ai_page import AIToAIPage
from .image_page import ImageGeneratorPage
from .video_page import VideoGeneratorPage
from .settings_page import SettingsPage
from .feedback_page import FeedbackPage
from .updates_page import UpdatesPage

__all__ = [
    "ChatPage",
    "AIToAIPage",
    "ImageGeneratorPage",
    "VideoGeneratorPage",
    "SettingsPage",
    "FeedbackPage",
    "UpdatesPage",
]
