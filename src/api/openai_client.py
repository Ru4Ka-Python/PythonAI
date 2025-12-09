"""OpenAI API client wrapper."""

from typing import Optional, List, Dict, Generator
from dataclasses import dataclass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None


@dataclass
class ChatMessage:
    """Represents a chat message."""
    role: str
    content: str


class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, api_key: str):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed. Run: pip install openai")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.api_key = api_key
    
    def set_api_key(self, api_key: str) -> None:
        """Update the API key."""
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key and self.client)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """Send a chat completion request."""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream
        )
        
        if stream:
            return response
        
        return response.choices[0].message.content
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """Send a streaming chat completion request."""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured")
        
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """Generate images using DALL-E."""
        if not self.is_configured():
            raise ValueError("OpenAI API key not configured")
        
        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        
        return [image.url for image in response.data]
