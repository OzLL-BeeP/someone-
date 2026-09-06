#!/usr/bin/env python3
# RAG - Retrieval-Augmented Generation

import os
import json
from pathlib import Path
from .config import RAG_DIR

class RAG:
    def __init__(self):
        self.knowledge = []
        self.load_knowledge()
    
    def load_knowledge(self):
        """Load all knowledge files"""
        try:
            RAG_DIR.mkdir(parents=True, exist_ok=True)
            docs_dir = RAG_DIR / "docs"
            docs_dir.mkdir(exist_ok=True)
            
            for file in docs_dir.glob("*.txt"):
                with open(file, 'r') as f:
                    content = f.read()
                    self.knowledge.append({
                        "file": file.name,
                        "content": content
                    })
        except Exception as e:
            print(f"Error loading knowledge: {e}")
    
    def search(self, query):
        """Search in knowledge base"""
        results = []
        for item in self.knowledge:
            if query.lower() in item["content"].lower():
                results.append(item)
        
        if results:
            return results[0]["content"][:1000]  # Return first 1000 chars
        return None
    
    def add_document(self, filename, content):
        """Add new document to knowledge base"""
        try:
            docs_dir = RAG_DIR / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = docs_dir / filename
            with open(filepath, 'w') as f:
                f.write(content)
            
            self.knowledge.append({
                "file": filename,
                "content": content
            })
            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
