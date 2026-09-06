import requests
import json

class Provider:
    def __init__(self, name, url, model, free=True):
        self.name = name
        self.url = url
        self.model = model
        self.free = free

PROVIDERS = [
    Provider("pollinations", "https://text.pollinations.ai/", "deepseek", free=True),
    Provider("pollinations", "https://text.pollinations.ai/", "gemini", free=True),
    Provider("pollinations", "https://text.pollinations.ai/", "kimi-k2", free=True),
]
