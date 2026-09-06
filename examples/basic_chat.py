#!/usr/bin/env python3
# Example: Basic Chat

from someone.main import SomeoneAI

ai = SomeoneAI()

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    response = ai.chat(user)
    print(f"Someone: {response}")
