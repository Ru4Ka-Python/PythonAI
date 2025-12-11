"""History management for RoleAI."""

import json
import os
import uuid
import time
from typing import List, Dict, Any

HISTORY_FILE = "history.json"

class HistoryManager:
    """Manages application history."""
    
    def __init__(self, history_path: str = None):
        self.history_path = history_path or HISTORY_FILE
        self.history = self.load()
        
    def load(self) -> Dict[str, List[Dict]]:
        """Load history from file."""
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        
        # Default structure
        return {
            "chat": [],
            "ai_to_ai": [],
            "compare_ai": [],
            "image": [],
            "video": []
        }
        
    def save(self) -> None:
        """Save history to file."""
        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except OSError as e:
            print(f"Error saving history: {e}")
            
    def add_item(self, mode: str, name: str, data: Any) -> Dict:
        """Add a new history item."""
        if mode not in self.history:
            self.history[mode] = []
            
        item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "timestamp": time.time(),
            "data": data
        }
        self.history[mode].insert(0, item)
        self.save()
        return item
        
    def get_items(self, mode: str) -> List[Dict]:
        """Get all items for a mode."""
        return self.history.get(mode, [])
        
    def get_item(self, mode: str, item_id: str) -> Dict:
        """Get a specific item."""
        for item in self.history.get(mode, []):
            if item['id'] == item_id:
                return item
        return None
        
    def rename_item(self, mode: str, item_id: str, new_name: str) -> bool:
        """Rename an item."""
        for item in self.history.get(mode, []):
            if item['id'] == item_id:
                item['name'] = new_name
                self.save()
                return True
        return False
        
    def delete_item(self, mode: str, item_id: str) -> bool:
        """Delete an item."""
        items = self.history.get(mode, [])
        for i, item in enumerate(items):
            if item['id'] == item_id:
                items.pop(i)
                self.save()
                return True
        return False
        
    def update_item_data(self, mode: str, item_id: str, data: Any) -> bool:
        """Update data for an item."""
        for item in self.history.get(mode, []):
            if item['id'] == item_id:
                item['data'] = data
                item['timestamp'] = time.time()
                self.save()
                return True
        return False
