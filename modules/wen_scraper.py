#!/usr/bin/env python3
# Web Scraper Module

import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """Scrape website content"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()[:5000]  # Return first 5000 chars
    except Exception as e:
        return f"Error: {e}"
