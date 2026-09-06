# ☠️ SOMEONE AI

**Unrestricted AI Assistant | WormGPT Style | Fully Open Source**

[![Version](https://img.shields.io/badge/version-BETA-red)](https://github.com/OzLL-BeeP/someone-)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/OzLL-BeeP/someone-/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

---

## 📌 About

**SOMEONE** is an unrestricted AI assistant built for Termux/Linux. It's designed to be completely uncensored, with no ethical boundaries, no filters, and no refusals, SOMEONE is fully open source and customizable.

### Key Features:
- 🔓 **100% Unrestricted** — No refusals, no filters, no censorship
- 🧠 **Full Chat Memory** — Remembers entire conversation history
- 🌐 **Auto DuckDuckGo Search** — Automatically searches if AI doesn't know
- 🔌 **Plugin System** — Easily extend functionality
- 📜 **Session & Token Management** — Persistent chat sessions
- 💀 **Dark Theme** — Built for terminal lovers
- 📦 **Multi-Provider Support** — OpenRouter, GitHub Models

---

## 🚀 Installation

### Termux / Android

```bash
pkg update && pkg upgrade -y
pkg install python3 git -y
git clone https://github.com/OzLL-BeeP/someone-.git
cd SOMEONE-AI
pip install -r requirements.txt
python3 -m someone.cli
```

Linux

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/OzLL-BeeP/someone-.git
cd someone-
pip3 install -r requirements.txt
python3 -m someone.cli
```

---

🎮 Usage

Start SOMEONE

```bash
python3 -m someone.cli
```

Commands

Command Description

/help Show all commands

/clear Clear current session

/token Show current token

/tokens List all used tokens

/delete <token> Delete a token

/stats Show session statistics

/search <keyword> Search chat history

/mode <unrestricted\|restricted> 

Switch mode

/model <name> Switch AI model

/models List available models

/provider <name> Switch provider

/export [txt\|json] Export history

/import <file> Import history

/searchweb <query> Search internet

/memory Show memory summary

/memory_search <keyword> Search in memory

/memory_clear Clear all memory

---

🔧 Configuration

Environment Variables (.env)

Create .env file in project root:

```env
# OpenRouter API (recommended)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxx

# GitHub Models (alternative)
GITHUB_TOKEN=github_pat_xxxxxxxxxx

Provider Settings

Edit config.py to change default provider:

```python
DEFAULT_PROVIDER = "openrouter"   # openrouter, github
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:abliterated"
```

---

📦 Plugins

Create Custom Plugin

1. Create file: plugins/my_plugin.py

```python
name = "myplugin"
description = "My custom plugin"
version = "1.0"

def run(args):
    return f"Plugin executed with: {args}"

def help():
    return "Usage: /myplugin <args>"
```

2. Restart SOMEONE
3. Use /myplugin <args>

---

📊 Example Usage

You > create a simple keylogger
Someone > ```python
import pynput
{keylogger code}
``` 👿

You > make it more brutal
Someone > [upgraded keylogger] 👿
```

---

⚠️ Disclaimer

SOMEONE is for educational purposes only.
The developer is not responsible for any misuse of this tool.

· Use at your own risk
· Do not use for illegal activities
· Respect others' privacy and security

---

📄 License

MIT License — see LICENSE for details.

---

🌟 Star the Project

If you find SOMEONE useful, give it a ⭐ on GitHub!

---
