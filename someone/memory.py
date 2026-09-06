import json
import os
import random
import string
from datetime import datetime
from pathlib import Path

# ============================================
# SESSION DIR
# ============================================
SESSION_DIR = Path("data/sessions")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# SESSION MANAGER — SAVE, LOAD, LIST, DELETE
# ============================================
def save_session(token, history, images=None):
    """Simpan sesi lengkap (chat + gambar)"""
    if images is None:
        images = []
    filename = SESSION_DIR / f"{token}.json"
    data = {
        "token": token,
        "timestamp": datetime.now().isoformat(),
        "history": history,
        "images": images
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return filename

def load_session(token):
    """Load sesi berdasarkan token"""
    filename = SESSION_DIR / f"{token}.json"
    if filename.exists():
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def list_sessions():
    """List semua sesi"""
    return [f.stem for f in SESSION_DIR.glob("*.json")]

def delete_session(token):
    """Hapus sesi berdasarkan token"""
    filename = SESSION_DIR / f"{token}.json"
    if filename.exists():
        filename.unlink()
        return True
    return False

# ============================================
# MEMORY MANAGER — CHAT HISTORY
# ============================================
class MemoryManager:
    def __init__(self, history_file="data/history.txt", token_db="data/tokens.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.token_db = Path(token_db)
        self.token_db.parent.mkdir(parents=True, exist_ok=True)
        self.current_token = None
        self._load_token_db()
    
    def _load_token_db(self):
        if self.token_db.exists():
            with open(self.token_db, 'r') as f:
                self.tokens = json.load(f)
        else:
            self.tokens = {"used": [], "available": []}
    
    def _save_token_db(self):
        with open(self.token_db, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def generate_token(self):
        chars = string.ascii_uppercase + string.digits
        for _ in range(100):
            code = ''.join(random.choices(chars, k=16))
            token = f"sx{code}"
            if token not in self.tokens["used"]:
                self.tokens["used"].append(token)
                self._save_token_db()
                return token
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        token = f"sx{timestamp}"
        self.tokens["used"].append(token)
        self._save_token_db()
        return token
    
    def delete_token(self, token):
        if token in self.tokens["used"]:
            self.tokens["used"].remove(token)
            self._save_token_db()
            return True
        return False
    
    def is_token_used(self, token):
        return token in self.tokens["used"]
    
    def get_all_used_tokens(self):
        return self.tokens["used"]
    
    def set_token(self, token, password=None):
        if self.is_token_used(token):
            self.current_token = token
            return True, "Token set"
        return False, "Token not found"
    
    def get_token(self):
        if not self.current_token:
            self.current_token = self.generate_token()
        return self.current_token
    
    def save_message(self, role, content, token=None):
        if not token:
            token = self.get_token()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{token}] {role}: {content}\n"
        
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        return token
    
    def get_history_by_token(self, token, password=None):
        if not self.history_file.exists():
            return [], None
        
        history = []
        with open(self.history_file, 'r', encoding='utf-8') as f:
            for line in f:
                if token in line:
                    parts = line.split('] ')
                    if len(parts) >= 3:
                        timestamp = parts[0][1:]
                        role_content = parts[2].split(': ', 1)
                        if len(role_content) == 2:
                            role = role_content[0]
                            content = role_content[1].strip()
                            history.append({
                                "timestamp": timestamp,
                                "role": role,
                                "content": content
                            })
        return history, None
    
    def validate_token(self, token):
        import re
        return bool(re.match(r'^sx[A-Z0-9]{16}$', token))
    
    def clear_history(self):
        """Hapus semua history"""
        try:
            if self.history_file.exists():
                self.history_file.unlink()
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
