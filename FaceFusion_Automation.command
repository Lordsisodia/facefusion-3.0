#!/bin/bash

# FaceFusion Automation Launcher for macOS
# Double-click this file to start the automation system

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

echo "🎭 FaceFusion Automation Launcher"
echo "=================================="
echo "📁 Working directory: $DIR"
echo ""

# Check if Python 3.11 is available
if command -v /opt/homebrew/bin/python3.11 &> /dev/null; then
    echo "✅ Python 3.11 found"
    /opt/homebrew/bin/python3.11 launch_automation.py
else
    echo "❌ Python 3.11 not found"
    echo ""
    echo "📋 Please install Python 3.11 first:"
    echo "1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "2. Install Python: brew install python@3.11"
    echo ""
    echo "Press any key to exit..."
    read -n 1
fi