#!/bin/bash

echo "Installing SOMEONE AI for Linux..."
echo "========================================"

sudo apt update
sudo apt install python3 python3-pip -y

pip3 install -r requirements.txt

echo "✅ Installation complete!"
