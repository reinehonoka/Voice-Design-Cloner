#!/bin/bash
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo "  VoiceDesignCloner - Setup"
echo "============================================"
echo ""

# --- Python version selection ---
PYTHON_CMD=""

# Look for a compatible version (3.12 preferred, then 3.11, 3.10)
for VER in 3.12 3.11 3.10; do
    if python$VER --version > /dev/null 2>&1; then
        PYTHON_CMD="python$VER"
        echo "[INFO] Found compatible Python $VER."
        break
    fi
done

# No compatible version found -- try plain python3
if [ -z "$PYTHON_CMD" ]; then
    if ! python3 --version > /dev/null 2>&1; then
        echo "[ERROR] Python not found. Please install Python 3.10-3.12."
        echo "https://www.python.org/downloads/release/python-3120/"
        exit 1
    fi
    PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MINOR" -gt 12 ]; then
        echo "[WARN] Python $PY_VER is not officially supported (recommended: 3.10-3.12)."
        echo "[WARN] You may encounter errors during setup or at runtime."
        echo ""
        read -p "Continue anyway? (y/N): " CONT
        if [ "$CONT" != "y" ] && [ "$CONT" != "Y" ]; then
            echo "Aborted."
            exit 1
        fi
    fi
    PYTHON_CMD="python3"
    echo "[INFO] Using python: $PY_VER"
fi

# Create venv
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
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

# ============================================
#   Irodori-TTS (optional, GPU only)
# ============================================
echo ""
echo "============================================"
echo "  Irodori-TTS Setup (optional)"
echo "============================================"
if ! nvidia-smi > /dev/null 2>&1; then
    echo "[INFO] No NVIDIA GPU detected. Skipping Irodori-TTS (GPU required)."
elif ! command -v git > /dev/null 2>&1; then
    echo "[WARN] git not found. Skipping Irodori-TTS."
    echo "[WARN] Install git and re-run setup to enable Irodori."
else
    mkdir -p engines
    if [ ! -d "engines/Irodori-TTS" ]; then
        echo "[INFO] Cloning Irodori-TTS..."
        if ! git clone https://github.com/Aratako/Irodori-TTS.git engines/Irodori-TTS; then
            echo "[WARN] git clone failed. Skipping Irodori-TTS."
        fi
    else
        echo "[INFO] engines/Irodori-TTS already exists. Skipping clone."
    fi

    if [ -d "engines/Irodori-TTS" ]; then
        echo "[INFO] Installing uv into main venv..."
        if pip install -U uv; then
            echo "[INFO] Running uv sync --extra cu128 in engines/Irodori-TTS..."
            (cd engines/Irodori-TTS && uv sync --extra cu128)
            if [ $? -eq 0 ]; then
                echo "[INFO] Irodori-TTS setup complete."
            else
                echo "[WARN] uv sync failed. Irodori-TTS may not be usable."
            fi
        else
            echo "[WARN] uv installation failed. Skipping Irodori-TTS."
        fi
    fi
fi

echo ""
echo "============================================"
echo "  Setup complete! Run app.sh to start."
echo "============================================"
