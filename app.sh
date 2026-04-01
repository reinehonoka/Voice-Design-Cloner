#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "[ERROR] venv not found. Please run setup.sh first."
    exit 1
fi

source venv/bin/activate
echo "[INFO] Starting VoiceDesignCloner..."
echo "[INFO] Browser will open automatically. If not, go to http://127.0.0.1:7860"
python app.py
