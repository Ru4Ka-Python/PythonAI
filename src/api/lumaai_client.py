"""LumaAI API client wrapper for video generation."""

import time
from typing import Optional
from dataclasses import dataclass
from enum import Enum

try:
    from lumaai import LumaAI
    LUMAAI_AVAILABLE = True
except ImportError:
    LUMAAI_AVAILABLE = False
    LumaAI = None


class VideoStatus(Enum):
    """Video generation status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class VideoResult:
    """Result of video generation."""
    id: str
    status: VideoStatus
    url: Optional[str] = None
    error: Optional[str] = None


class LumaAIClient:
    """Client for interacting with LumaAI API."""
    
    def __init__(self, api_key: str):
        if not LUMAAI_AVAILABLE:
            raise ImportError("LumaAI package is not installed. Run: pip install lumaai")
        self.api_key = api_key
        self.client = LumaAI(auth_token=api_key) if api_key else None
    
    def set_api_key(self, api_key: str) -> None:
        """Update the API key."""
        self.api_key = api_key
        self.client = LumaAI(auth_token=api_key) if api_key else None
    
    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key and self.client)
    
    def generate_video(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        loop: bool = False
    ) -> VideoResult:
        """Start video generation."""
        if not self.is_configured():
            raise ValueError("LumaAI API key not configured")
        
        try:
            generation = self.client.generations.create(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                loop=loop
            )
            
            return VideoResult(
                id=generation.id,
                status=VideoStatus.PENDING
            )
        except Exception as e:
            return VideoResult(
                id="",
                status=VideoStatus.FAILED,
                error=str(e)
            )
    
    def get_video_status(self, generation_id: str) -> VideoResult:
        """Check status of video generation."""
        if not self.is_configured():
            raise ValueError("LumaAI API key not configured")
        
        try:
            generation = self.client.generations.get(id=generation_id)
            
            if generation.state == "completed":
                return VideoResult(
                    id=generation_id,
                    status=VideoStatus.COMPLETED,
                    url=generation.assets.video if generation.assets else None
                )
            elif generation.state == "failed":
                return VideoResult(
                    id=generation_id,
                    status=VideoStatus.FAILED,
                    error=generation.failure_reason
                )
            else:
                return VideoResult(
                    id=generation_id,
                    status=VideoStatus.PROCESSING
                )
        except Exception as e:
            return VideoResult(
                id=generation_id,
                status=VideoStatus.FAILED,
                error=str(e)
            )
    
    def wait_for_completion(
        self,
        generation_id: str,
        timeout: int = 300,
        poll_interval: int = 5,
        callback=None
    ) -> VideoResult:
        """Wait for video generation to complete."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.get_video_status(generation_id)
            
            if callback:
                callback(result)
            
            if result.status in (VideoStatus.COMPLETED, VideoStatus.FAILED):
                return result
            
            time.sleep(poll_interval)
        
        return VideoResult(
            id=generation_id,
            status=VideoStatus.FAILED,
            error="Timeout waiting for video generation"
        )
