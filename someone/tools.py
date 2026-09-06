#!/usr/bin/env python3
# Tools - Search Only (Image Generation Disabled)
# By: K1dz

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SAVE_DIR = Path("data/generated")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# INTERNET SEARCH (DUCKDUCKGO API)
# ============================================
def search_web(query):
    """Cari informasi dari internet pake DuckDuckGo"""
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Ambil AbstractText
            abstract = data.get("AbstractText", "")
            if abstract:
                return abstract
            
            # Ambil RelatedTopics
            topics = data.get("RelatedTopics", [])
            if topics:
                for topic in topics[:3]:
                    text = topic.get("Text", "")
                    if text:
                        return text
            
            # Ambil dari Infobox
            infobox = data.get("Infobox", {})
            if infobox:
                content = infobox.get("content", [])
                if content:
                    return "\n".join([c.get("value", "") for c in content[:5]])
            
            return "No results found."
        else:
            return f"Search error: {response.status_code}"
    except Exception as e:
        return f"Search error: {str(e)}"
