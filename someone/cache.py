import json
import hashlib
from pathlib import Path
from .config import DATA_DIR

CACHE_DIR = DATA_DIR / "cache"

class Cache:
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def get_key(self, prompt, model):
        return hashlib.md5(f"{prompt}:{model}".encode()).hexdigest()
    
    def get(self, key):
        filepath = CACHE_DIR / f"{key}.json"
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f).get("response")
        return None
    
    def set(self, key, response):
        filepath = CACHE_DIR / f"{key}.json"
        with open(filepath, "w") as f:
            json.dump({"response": response}, f)
