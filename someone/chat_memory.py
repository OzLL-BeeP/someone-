#!/usr/bin/env python3
# Chat Memory - Full Conversation Memory
# By: K1dz

import json
import os
from datetime import datetime
from pathlib import Path

class ChatMemory:
    def __init__(self, token):
        self.token = token
        self.memory_dir = Path("data/memories")
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_dir / f"{token}.json"
        self.history = []
        self._load()
    
    def _load(self):
        """Load memory dari file"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    print(f"[🧠] Memory loaded: {len(self.history)} messages")
            except:
                self.history = []
        else:
            self.history = []
    
    def _save(self):
        """Save memory ke file"""
        data = {
            "token": self.token,
            "timestamp": datetime.now().isoformat(),
            "history": self.history
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add(self, role, content):
        """Tambah pesan ke memory"""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_context(self, limit=20):
        """Dapatkan konteks untuk AI (bisa diatur limit)"""
        if not self.history:
            return []
        
        # Ambil N pesan terakhir
        return self.history[-limit:] if limit > 0 else self.history
    
    def get_full_context(self):
        """Dapatkan SEMUA history (unlimited)"""
        return self.history
    
    def clear(self):
        """Hapus semua memory"""
        self.history = []
        if self.memory_file.exists():
            self.memory_file.unlink()
    
    def get_summary(self):
        """Dapatkan ringkasan memory"""
        if not self.history:
            return "No memory yet."
        
        total = len(self.history)
        roles = {}
        for msg in self.history:
            role = msg.get("role", "unknown")
            roles[role] = roles.get(role, 0) + 1
        
        result = f"🧠 Memory Summary:\n"
        result += f"  Total messages: {total}\n"
        result += f"  User: {roles.get('user', 0)}\n"
        result += f"  Assistant: {roles.get('assistant', 0)}\n"
        result += f"  System: {roles.get('system', 0)}\n"
        result += f"  Last message: {self.history[-1].get('content', '')[:50]}..."
        return result
    
    def search(self, keyword):
        """Cari dalam memory"""
        results = []
        for msg in self.history:
            if keyword.lower() in msg.get("content", "").lower():
                results.append(msg)
        return results
