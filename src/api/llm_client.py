"""Unified LLM Client for OpenAI and Gemini."""

from typing import Optional, List, Dict, Generator
import time

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class LLMClient:
    """Client for interacting with OpenAI and Gemini APIs."""
    
    def __init__(self, openai_api_key: str = "", gemini_api_key: str = ""):
        self.openai_key = openai_api_key
        self.gemini_key = gemini_api_key
        
        self.openai_client = None
        if openai_api_key and OPENAI_AVAILABLE:
            self.openai_client = OpenAI(api_key=openai_api_key)
            
        if gemini_api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_api_key)
    
    def set_api_keys(self, openai_key: str = "", gemini_key: str = ""):
        """Update API keys."""
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        
        if openai_key and OPENAI_AVAILABLE:
            self.openai_client = OpenAI(api_key=openai_key)
            
        if gemini_key and GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_key)

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        provider: str = "openai",
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """Send a streaming chat completion request."""
        
        if provider == "openai":
            if not self.openai_client:
                raise ValueError("OpenAI API key not configured")
            
            stream = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        elif provider == "gemini":
            if not self.gemini_key or not GEMINI_AVAILABLE:
                raise ValueError("Gemini API key not configured or package missing")
            
            # Convert messages to Gemini format
            # Gemini expects history as list of contents, and a final message
            # But simple chat API: model.generate_content(stream=True)
            
            g_model = genai.GenerativeModel(model)
            
            # Simple conversion for now: Concatenate or use chat session
            # For strict role adherence, chat session is better.
            
            history = []
            last_message = ""
            
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg == messages[-1] and msg["role"] == "user":
                    last_message = msg["content"]
                else:
                    history.append({"role": role, "parts": [msg["content"]]})
            
            if not last_message and messages:
                 # Handle case where last message wasn't user (e.g. continue) - unlikely for this app
                 last_message = messages[-1]["content"]

            chat = g_model.start_chat(history=history)
            response = chat.send_message(last_message, stream=True, generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature
            ))
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text

    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1
    ) -> List[str]:
        """Generate images using DALL-E (Gemini image gen not requested explicitly but possible)."""
        # Assuming OpenAI for image generation as per requirements
        if not self.openai_client:
             raise ValueError("OpenAI API key not configured")
             
        response = self.openai_client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )
        return [image.url for image in response.data]
