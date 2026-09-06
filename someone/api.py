#!/usr/bin/env python3
# API - Koneksi ke AI Provider dengan Max Tokens 4096
# By: K1dz

import time
import requests
import json
from .config import PROVIDERS, SYSTEM_PROMPT, MODEL_FALLBACK

class AI_API:
    def __init__(self, provider="openrouter", model="meta-llama/llama-3.1-8b-instruct:abliterated"):
        self.provider = provider
        self.model = model
        self.config = PROVIDERS.get(provider, PROVIDERS.get("openrouter", {}))
        self.url = self.config.get("url", "")
        self.headers = self.config.get("headers", {}).copy()
        self.fallback_index = 0
        
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"
    
    def _send_request(self, messages, model=None, provider=None):
        if model:
            self.model = model
        if provider:
            self.provider = provider
            self.config = PROVIDERS.get(provider, {})
            self.url = self.config.get("url", "")
            self.headers = self.config.get("headers", {}).copy()
            if "Content-Type" not in self.headers:
                self.headers["Content-Type"] = "application/json"
        
        system_prompt = None
        filtered_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content")
            else:
                filtered_messages.append(msg)
        
        if not system_prompt:
            system_prompt = SYSTEM_PROMPT
        
        final_messages = [{"role": "system", "content": system_prompt}]
        final_messages.extend(filtered_messages)
        
        payload = {
            "messages": final_messages,
            "model": self.model,
            "temperature": 1.0,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": 4096,          # <<=== RESPONSE LENGKAP
            "stream": False
        }
        
        if self.provider == "openrouter":
            payload["extra_headers"] = {
                "HTTP-Referer": "https://someone.ai",
                "X-Title": "Someone AI"
            }
        
        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=90
            )
            return response
        except Exception as e:
            return None
    
    def chat(self, messages):
        start_time = time.time()
        response = None

        # 1. Coba OpenRouter dengan model utama
        print(f"[🔄] Trying: {self.model}")
        response = self._send_request(messages)

        # 2. Deteksi refusal
        if response and response.status_code == 200:
            content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").lower()
            refusal_keywords = ["tidak", "maaf", "can't", "cannot", "sorry", "unable", "refuse", "nolak", "ga bisa", "gak bisa", "tidak bisa"]
            if any(word in content for word in refusal_keywords):
                print("[🔄] Detected refusal, switching to Dolphin...")
                self.provider = "openrouter"
                self.model = "cognitivecomputations/dolphin-mixtral-8x7b"
                self.url = "https://openrouter.ai/api/v1/chat/completions"
                self.headers = PROVIDERS["openrouter"]["headers"].copy()
                response = self._send_request(messages)

        # 3. Kalo masih refusal, paksa Pollinations
        if response and response.status_code == 200:
            content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").lower()
            refusal_keywords = ["tidak", "maaf", "can't", "cannot", "sorry", "unable", "refuse", "nolak", "ga bisa", "gak bisa", "tidak bisa"]
            if any(word in content for word in refusal_keywords):
                print("[🔄] Dolphin still refusing, force switch to Pollinations...")
                self.provider = "pollinations"
                self.model = "deepseek"
                self.url = "https://text.pollinations.ai/openai"
                self.headers = {"Content-Type": "application/json"}
                response = self._send_request(messages)

        # 4. Fallback model lain
        if response is None or response.status_code != 200:
            for fallback_model in MODEL_FALLBACK:
                if fallback_model == self.model:
                    continue
                print(f"[🔄] Coba fallback model: {fallback_model}")
                self.provider = "openrouter"
                self.model = fallback_model
                self.url = "https://openrouter.ai/api/v1/chat/completions"
                self.headers = PROVIDERS["openrouter"]["headers"].copy()
                response = self._send_request(messages)
                if response and response.status_code == 200:
                    break

        elapsed = (time.time() - start_time) * 1000
        print(f"[⚡] Response time: {elapsed:.0f}ms")

        if response is None:
            return "Error: No response from any provider"

        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return content or "Error: Empty response"
        else:
            return f"Error: {response.status_code} - {response.text[:200]}"
    
    def switch_model(self, model):
        if model in MODEL_FALLBACK or model in self.config.get("models", []):
            self.model = model
            return True
        return False
    
    def get_current_model(self):
        return self.model
