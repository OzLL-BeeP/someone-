#!/usr/bin/env python3
# Utils - Utility Functions

import os
import json
from datetime import datetime

def timestamp():
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_json(data, filepath):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    """Load data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def ensure_dir(path):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)
