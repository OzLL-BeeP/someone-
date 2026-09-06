#!/usr/bin/env python3
# SOMEONE AI - CLI Interface
# By: K1dz

import os
import sys
import getpass
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from .main import SomeoneAI
from .memory import save_session, list_sessions, load_session

load_dotenv()

# ============================================
# CLEAR SCREEN
# ============================================
def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

# ============================================
# BANNER
# ============================================
def show_banner(ai):
    clear_screen()
    print("\033[1;30m" + "="*55 + "\033[0m")
    print("\033[1;30m  ☠️  S O M E O N E   A I  [BETA]  ☠️\033[0m")
    print("\033[1;30m" + "="*55 + "\033[0m")
    print(f"  Token   : {ai.current_token}")
    print(f"  Model   : {ai.model}")
    print(f"  Provider: {ai.provider}")
    print(f"  Mode    : {ai.mode.upper()}")
    print(f"  History : {len(ai.history)} messages")
    print(f"  Memory  : {len(ai.chat_memory.history)} messages")
    print("\033[1;30m" + "-"*55 + "\033[0m")
    print("  Commands: /help  | exit")
    print("\033[1;30m" + "="*55 + "\033[0m")
    print()

# ============================================
# SHOW STATUS
# ============================================
def show_status(ai):
    return f"""
╔═══════════════════════════════════════════╗
║              STATUS SOMEONE               ║
╠═══════════════════════════════════════════╣
║ Token    : {ai.current_token}
║ Model    : {ai.model}
║ Provider : {ai.provider}
║ Mode     : {ai.mode.upper()}
║ LoRA     : {ai.lora_id if ai.lora_id else 'None'}
║ History  : {len(ai.history)} messages
║ Memory   : {len(ai.chat_memory.history)} messages
║ Sessions : {len(list_sessions())}
╚═══════════════════════════════════════════╝
"""

# ============================================
# SHOW HISTORY
# ============================================
def show_history(ai, limit=10):
    if not ai.history:
        return "📭 No history yet."
    
    result = "📜 Last messages:\n" + "-"*40 + "\n"
    for msg in ai.history[-limit:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if len(content) > 60:
            content = content[:60] + "..."
        result += f"[{role.upper()}] {content}\n"
    result += "-"*40
    return result

# ============================================
# SHOW SESSIONS
# ============================================
def show_sessions():
    sessions = list_sessions()
    if not sessions:
        return "📭 No sessions found."
    result = "📁 Saved sessions:\n" + "-"*30 + "\n"
    for s in sessions:
        result += f"  - {s}\n"
    result += "-"*30
    return result

# ============================================
# MAIN
# ============================================
def main():
    ai = SomeoneAI()
    show_banner(ai)
    
    while True:
        try:
            user = input("\033[1;33mYou > \033[0m")
            
            # Exit
            if user.lower() in ["exit", "quit", "keluar"]:
                save_session(ai.current_token, ai.history)
                print("\033[1;30mBye! 👿\033[0m")
                break
            
            # Clear
            if user.lower() in ["clear", "cls"]:
                show_banner(ai)
                continue
            
            # Status
            if user.lower() == "/status":
                print(show_status(ai))
                continue
            
            # History
            if user.lower() == "/history":
                print(show_history(ai))
                continue
            
            # Sessions list
            if user.lower() == "/sessions":
                print(show_sessions())
                continue
            
            # Memory summary
            if user.lower() == "/memory":
                print(ai.chat_memory.get_summary())
                continue
            
            # Memory search
            if user.lower().startswith("/memory_search"):
                keyword = user[14:].strip()
                if keyword:
                    results = ai.chat_memory.search(keyword)
                    if results:
                        print("🔍 Search results:")
                        for r in results[:10]:
                            role = r.get('role', 'unknown')
                            content = r.get('content', '')[:100]
                            print(f"  [{role.upper()}] {content}...")
                    else:
                        print("No results found.")
                else:
                    print("❌ Usage: /memory_search <keyword>")
                continue
            
            # Memory clear
            if user.lower() == "/memory_clear":
                ai.chat_memory.clear()
                print("🧠 Memory cleared!")
                continue
            
            # Load session
            if user.lower().startswith("/load"):
                parts = user.split()
                if len(parts) >= 2:
                    token = parts[1]
                    data = load_session(token)
                    if data:
                        ai.current_token = token
                        ai.history = data.get("history", [])
                        show_banner(ai)
                        print(f"✅ Session {token} loaded! ({len(ai.history)} messages)")
                    else:
                        print(f"❌ Session {token} not found.")
                else:
                    print("❌ Usage: /load <token>")
                continue
            
            # Delete session
            if user.lower().startswith("/delete_session"):
                parts = user.split()
                if len(parts) >= 2:
                    token = parts[1]
                    from .memory import delete_session
                    if delete_session(token):
                        print(f"✅ Session {token} deleted.")
                    else:
                        print(f"❌ Session {token} not found.")
                else:
                    print("❌ Usage: /delete_session <token>")
                continue
            
            # !set command
            if user.lower().startswith("!set"):
                parts = user.split()
                if len(parts) >= 2:
                    token = parts[1]
                    password = parts[2] if len(parts) >= 3 else getpass.getpass("Password: ")
                    response = ai.set_token(token, password)
                    print(f"\033[1;30mSomeone > \033[0m{response}")
                    show_banner(ai)
                else:
                    print("\033[1;30mSomeone > \033[0mUsage: !set sx... [password]")
                continue
            
            # Refresh
            if user.lower() == "/refresh":
                show_banner(ai)
                continue
            
            # Chat
            response = ai.chat(user)
            print(f"\033[1;30mSomeone > \033[0m{response}")
            print()
            
            # Auto save
            save_session(ai.current_token, ai.history)
            
        except KeyboardInterrupt:
            save_session(ai.current_token, ai.history)
            print("\n\033[1;30mBye! 👿\033[0m")
            break
        except Exception as e:
            print(f"\033[1;31mError: {e}\033[0m")

if __name__ == "__main__":
    main()
