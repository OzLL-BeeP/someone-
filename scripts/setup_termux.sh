#!/bin/bash

echo " Installing SOMEONE AI for Termux..."
echo "========================================"

# Update packages
pkg update && pkg upgrade -y

# Install Python
pkg install python -y

# Install dependencies
pip install requests

# Clone atau setup
echo "✅ Installation complete!"
echo "========================================"
echo "Run: python -m someone.cli"
