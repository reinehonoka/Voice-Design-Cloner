#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "[ERROR] venv not found. Please run setup.sh first."
    exit 1
fi

source venv/bin/activate
echo "[INFO] Starting VoiceDesignCloner..."
echo "[INFO] Browser will open automatically."
echo "[INFO] Default URL: http://127.0.0.1:7860"
echo "[INFO] If 7860 is busy, the app will use the next free port."
python app.py
