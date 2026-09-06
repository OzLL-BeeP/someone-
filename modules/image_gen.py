#!/usr/bin/env python3
# Image Generation Module

import requests

def generate_image(prompt):
    """Generate image from prompt"""
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    return url
