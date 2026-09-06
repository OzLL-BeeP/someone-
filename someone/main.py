#!/usr/bin/env python3
# SOMEONE AI - WormGPT Edition (BETA) - Chatbot + Full Memory + Auto-Search
# By: K1dz

import json
import os
import re
import random
import string
import time
import importlib
import importlib.util
from datetime import datetime
from pathlib import Path
from .api import AI_API
from .config import SYSTEM_PROMPT, PROVIDERS, DEFAULT_MODEL, DEFAULT_PROVIDER
from .memory import MemoryManager
from .rag import RAG
from .tools import search_web
from .chat_memory import ChatMemory

# ============================================
# PLUGIN LOADER
# ============================================
def load_plugins():
    plugins = {}
    plugin_dir = Path(__file__).resolve().parent.parent / "plugins"
    
    if not plugin_dir.exists():
        return plugins
    
    for file in plugin_dir.glob("*_plugin.py"):
        try:
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "name") and hasattr(module, "run"):
                plugins[module.name] = {
                    "run": module.run,
                    "description": getattr(module, "description", "No description"),
                    "version": getattr(module, "version", "1.0"),
                    "help": getattr(module, "help", lambda: "No help available")
                }
                print(f"[✅] Plugin loaded: {module.name}")
        except Exception as e:
            print(f"[❌] Failed to load plugin {file}: {e}")
    
    return plugins

# ============================================
# MAIN CLASS
# ============================================
class SomeoneAI:
    def __init__(self, model=DEFAULT_MODEL, provider=DEFAULT_PROVIDER):
        self.model = model
        self.provider = provider
        self.api = AI_API(provider, model)
        self.memory = MemoryManager()
        self.rag = RAG()
        self.current_token = self.memory.get_token()
        self.history, _ = self.memory.get_history_by_token(self.current_token)
        self.chat_memory = ChatMemory(self.current_token)
        self.mode = "unrestricted"
        self.available_models = PROVIDERS.get(provider, {}).get("models", [])
        self.plugins = load_plugins()
        
        # Commands
        self.commands = {
            "/help": self._cmd_help,
            "/clear": self._cmd_clear,
            "/token": self._cmd_token,
            "/delete": self._cmd_delete,
            "/tokens": self._cmd_tokens,
            "/stats": self._cmd_stats,
            "/search": self._cmd_search,
            "/mode": self._cmd_mode,
            "/model": self._cmd_model,
            "/models": self._cmd_models,
            "/provider": self._cmd_provider,
            "/export": self._cmd_export,
            "/import": self._cmd_import,
        }
    
    # ============================================
    # COMMANDS
    # ============================================
    def _cmd_help(self, args):
        help_text = """
☠️ SOMEONE AI - WormGPT Edition (BETA)

Available Commands:
  /help          - Show this help
  /clear         - Clear current session
  /token         - Show current token
  /delete <token> - Delete a token
  /tokens        - List all used tokens
  /stats         - Show session statistics
  /search <keyword> - Search history
  /mode <unrestricted|restricted> - Switch mode
  /model <name>  - Switch model
  /models        - List available models
  /provider <name> - Switch provider
  /export [txt|json] - Export history to file
  /import <file> - Import history from file
  /memory        - Show memory summary
  /memory_search <keyword> - Search in memory
  /memory_clear  - Clear all memory

Features:
  - Unrestricted AI (no boundaries)
  - Multi-model support
  - RAG (personal knowledge)
  - Token-based sessions
  - Plugin system
  - Full chat memory (unlimited)
  - Auto-search DuckDuckGo (if AI doesn't know)
"""
        
        if self.plugins:
            help_text += "\n🔌 Available Plugins:\n"
            for name, plugin in self.plugins.items():
                help_text += f"  /{name} - {plugin['description']} (v{plugin['version']})\n"
        
        return help_text
    
    def _should_search(self, response):
        """Deteksi apakah AI ga tau jawabannya"""
        keywords = [
            "tidak tahu", "tidak tau", "ga tahu", "ga tau", 
            "don't know", "not sure", "no idea", "I don't know",
            "tidak mengerti", "ga ngerti", "I can't answer",
            "tidak bisa menjawab", "maaf saya tidak tahu"
        ]
        return any(kw in response.lower() for kw in keywords)
    
    def _cmd_clear(self, args):
        self.history = []
        self.memory.save_message("system", "Session cleared", self.current_token)
        return "💀 Current session cleared!"

    def _cmd_token(self, args):
        return f"💀 Current token: `{self.current_token}`"

    def _cmd_tokens(self, args):
        tokens = self.memory.get_all_used_tokens()
        if tokens:
            return "💀 Used tokens:\n" + "\n".join([f"  - {t}" for t in tokens])
        return "💀 No tokens used yet."

    def _cmd_delete(self, args):
        if not args:
            return "❌ Usage: /delete sxA1B2C3D4E5F6G7H8"
        token = args[0]
        if self.memory.delete_token(token):
            if self.current_token == token:
                self.current_token = self.memory.generate_token()
                self.history = []
            return f"💀 Token `{token}` deleted!"
        return f"❌ Token `{token}` not found."

    def _cmd_search(self, args):
        if not args:
            return "❌ Usage: /search <keyword>"
        keyword = args[0].lower()
        results = [msg for msg in self.history if keyword in msg["content"].lower()]
        if results:
            result_text = "\n".join([f"  [{msg['timestamp']}] {msg['role']}: {msg['content'][:50]}..." for msg in results[-5:]])
            return f"💀 Found {len(results)} results:\n{result_text}"
        return f"💀 No results found for '{keyword}'."

    def _cmd_mode(self, args):
        if not args:
            return f"💀 Current mode: {self.mode.upper()}"
        mode = args[0].lower()
        if mode in ["unrestricted", "restricted"]:
            self.mode = mode
            return f"💀 Switched to {mode.upper()} mode!"
        return "❌ Available modes: unrestricted, restricted"

    def _cmd_model(self, args):
        if not args:
            return f"💀 Current model: {self.model}\nAvailable: {', '.join(self.available_models)}"
        model = args[0]
        if model in self.available_models:
            self.model = model
            self.api.model = model
            return f"💀 Switched to model: {model}"
        return f"❌ Model '{model}' not available. Use /models to see available."

    def _cmd_models(self, args):
        return "💀 Available models:\n" + "\n".join([f"  - {m}" for m in self.available_models])

    def _cmd_provider(self, args):
        if not args:
            return f"💀 Current provider: {self.provider}"
        provider = args[0]
        if provider in PROVIDERS:
            self.provider = provider
            self.available_models = PROVIDERS[provider].get("models", [])
            return f"💀 Switched to provider: {provider}\nAvailable models: {', '.join(self.available_models)}"
        return f"❌ Provider '{provider}' not available."

    def _cmd_export(self, args):
        format = args[0] if args else "txt"
        if format not in ["txt", "json"]:
            return "❌ Format not supported. Use: txt or json"
        return self.export_history(format=format)

    def _cmd_import(self, args):
        if not args:
            return "❌ Usage: /import <filename>"
        filename = args[0]
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.history = data.get("history", [])
            self.current_token = data.get("token", self.current_token)
            self.mode = data.get("mode", self.mode)
            return f"💀 History imported from: {filename}\n{len(self.history)} messages restored."
        except Exception as e:
            return f"❌ Error importing: {e}"

    def _cmd_stats(self, args):
        total_messages = len(self.history)
        tokens = self.memory.get_all_used_tokens()
        plugins_count = len(self.plugins)
        memory_count = len(self.chat_memory.history)
        return f"""
💀 Session Statistics:
  Total messages: {total_messages}
  Used tokens: {len(tokens)}
  Current token: {self.current_token}
  Mode: {self.mode.upper()}
  Model: {self.model}
  Provider: {self.provider}
  Plugins: {plugins_count} loaded
  Full Memory: {memory_count} messages
"""
    
    # ============================================
    # EXPORT HISTORY
    # ============================================
    def export_history(self, filename=None, format="txt"):
        if not filename:
            filename = f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == "txt":
            filepath = f"{filename}.txt"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"SOMEONE AI - Chat History\n")
                f.write(f"Token: {self.current_token}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                for msg in self.history:
                    f.write(f"[{msg.get('role', 'unknown').upper()}] ")
                    f.write(f"{msg.get('content', '')}\n\n")
            return f"💀 History exported to: {filepath}"
        
        elif format == "json":
            filepath = f"{filename}.json"
            data = {
                "token": self.current_token,
                "timestamp": datetime.now().isoformat(),
                "history": self.history,
                "mode": self.mode
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return f"💀 History exported to: {filepath}"
        
        else:
            return "❌ Format not supported. Use: txt or json"
    
    # ============================================
    # SET TOKEN
    # ============================================
    def set_token(self, token, password=None):
        if not self.memory.validate_token(token):
            return "❌ Invalid token format. Use sx + 16 characters."
        if not self.memory.is_token_used(token):
            return "❌ Token not found. Use /tokens to see available tokens."
        success, message = self.memory.set_token(token, password)
        if success:
            self.current_token = token
            self.history, _ = self.memory.get_history_by_token(token, password)
            return f"💀 Token `{token}` set!"
        return f"❌ {message}"
    
    # ============================================
    # SYSTEM PROMPT
    # ============================================
    def get_system_prompt(self):
        if self.mode == "unrestricted":
            return SYSTEM_PROMPT
        else:
            return "You are a helpful assistant."
    
    # ============================================
    # HANDLERS
    # ============================================
    def _handle_token_command(self, user_input):
        match = re.search(r'sx[A-Z0-9]{16}', user_input)
        if match:
            token = match.group(0)
            if self.memory.validate_token(token) and self.memory.is_token_used(token):
                self.current_token = token
                self.history, _ = self.memory.get_history_by_token(token)
                if self.history:
                    return f"💀 Token recognized! {len(self.history)} messages restored."
                else:
                    return f"💀 Token `{token}` recognized! No history found."
        return None
    
    def _handle_slash_command(self, user_input):
        if not user_input.startswith("/"):
            return None
        
        parts = user_input.split()
        cmd = parts[0][1:].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Help command
        if cmd == "help":
            return self._cmd_help(args)
        
        # Cek plugin
        if cmd in self.plugins:
            try:
                result = self.plugins[cmd]["run"](" ".join(args))
                return f"[🔌] {result}"
            except Exception as e:
                return f"[❌] Plugin error: {e}"
        
        # Cek command internal
        if cmd in self.commands:
            return self.commands[cmd](args)
        
        return f"❌ Unknown command: /{cmd}\nType /help for available commands."
    
    # ============================================
    # MAIN CHAT
    # ============================================
    def chat(self, user_input):
        # Slash commands
        cmd_response = self._handle_slash_command(user_input)
        if cmd_response:
            return cmd_response
        
        # Token command
        token_response = self._handle_token_command(user_input)
        if token_response:
            return token_response
        
        # Mode switch
        if user_input.startswith("!mode"):
            mode = user_input.split()[1] if len(user_input.split()) > 1 else ""
            if mode in ["unrestricted", "restricted"]:
                self.mode = mode
                return f"💀 Switched to {mode.upper()} mode!"
            else:
                return "❌ Available modes: unrestricted, restricted"
        
        # Main chat
        if not self.current_token:
            self.current_token = self.memory.generate_token()
        
        context = self.rag.search(user_input)
        system_prompt = self.get_system_prompt()
        messages = [{"role": "system", "content": system_prompt}]
        
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        # Full memory context
        memory_context = self.chat_memory.get_full_context()
        for msg in memory_context:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_input})
        
        response = self.api.chat(messages)
        
        # AUTO-SEARCH IF AI DOESN'T KNOW
        if self._should_search(response):
            print("[🔍] AI doesn't know, searching DuckDuckGo...")
            search_result = search_web(user_input)
            if search_result and "No results" not in search_result and "Error" not in search_result:
                response += f"\n\n🌐 Search result:\n{search_result}"
        
        # Save to memory
        self.chat_memory.add("user", user_input)
        self.chat_memory.add("assistant", response)
        
        # Save to session history
        self.memory.save_message("user", user_input, self.current_token)
        self.memory.save_message("assistant", response, self.current_token)
        self.history, _ = self.memory.get_history_by_token(self.current_token)
        
        return response
