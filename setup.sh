#!/bin/bash
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo "  VoiceDesignCloner - Setup"
echo "============================================"
echo ""

# Check Python
if ! python3 --version > /dev/null 2>&1; then
    echo "[ERROR] Python not found. Please install Python 3.12."
    exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[INFO] venv already exists. Skipping."
fi

source venv/bin/activate

# Detect GPU and install PyTorch
echo ""
echo "[INFO] Checking GPU..."
if nvidia-smi > /dev/null 2>&1; then
    echo "[INFO] NVIDIA GPU detected. Installing CUDA version of PyTorch."
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "[INFO] No NVIDIA GPU detected. Installing CPU version of PyTorch."
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Upgrade packaging tools first. Some deps still use legacy setup.py flows.
echo ""
echo "[INFO] Upgrading pip/setuptools/wheel..."
pip install -U pip setuptools wheel

# sox may import numpy during metadata generation, so install it before requirements.
echo ""
echo "[INFO] Installing numpy first..."
pip install numpy

# Install dependencies
echo ""
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# faster-qwen3-tts (CUDA Graph acceleration, GPU only)
if nvidia-smi > /dev/null 2>&1; then
    echo "[INFO] Installing faster-qwen3-tts..."
    pip install faster-qwen3-tts
else
    echo "[INFO] No NVIDIA GPU detected. Skipping faster-qwen3-tts."
fi

echo ""
echo "============================================"
echo "  Setup complete! Run app.sh to start."
echo "============================================"
