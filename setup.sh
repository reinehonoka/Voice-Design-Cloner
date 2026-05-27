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

# Upgrade packaging tools first. Some deps still use legacy setup.py flows.
echo ""
echo "[INFO] Upgrading pip/setuptools/wheel..."
pip install -U pip wheel "setuptools<82"

# Detect GPU and install PyTorch
echo ""
echo "[INFO] Checking GPU..."
if nvidia-smi > /dev/null 2>&1; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n 1)
    TORCH_CUDA="${VDC_TORCH_CUDA:-}"
    if [ -z "$TORCH_CUDA" ]; then
        case "$GPU_NAME" in
            *"RTX 50"*|*"RTX PRO 50"*|*"RTX 5070"*|*"RTX 5080"*|*"RTX 5090"*)
                TORCH_CUDA="cu128"
                ;;
            *)
                TORCH_CUDA="cu118"
                ;;
        esac
    fi
    echo "[INFO] NVIDIA GPU detected: ${GPU_NAME:-unknown}"
    echo "[INFO] Installing PyTorch build: $TORCH_CUDA"
    echo "[INFO] Override with: VDC_TORCH_CUDA=cu128 ./setup.sh"
    pip install torch torchaudio --index-url "https://download.pytorch.org/whl/$TORCH_CUDA"
else
    echo "[INFO] No NVIDIA GPU detected. Installing CPU version of PyTorch."
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

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
    # Install Irodori under ~/.vdc-engines/ so it always lives on the home
    # filesystem and avoids issues with project dirs on exFAT/external drives.
    IRODORI_ROOT="$HOME/.vdc-engines/Irodori-TTS"
    mkdir -p "$HOME/.vdc-engines"
    if [ ! -d "$IRODORI_ROOT" ]; then
        echo "[INFO] Cloning Irodori-TTS to $IRODORI_ROOT ..."
        if ! git clone https://github.com/Aratako/Irodori-TTS.git "$IRODORI_ROOT"; then
            echo "[WARN] git clone failed. Skipping Irodori-TTS."
        fi
    else
        echo "[INFO] $IRODORI_ROOT already exists. Skipping clone."
    fi

    if [ -d "$IRODORI_ROOT" ]; then
        echo "[INFO] Installing uv into main venv..."
        if pip install -U uv; then
            echo "[INFO] Running uv sync --extra cu128 in $IRODORI_ROOT ..."
            (
                cd "$IRODORI_ROOT" || exit 1
                OLD_VIRTUAL_ENV="${VIRTUAL_ENV:-}"
                unset VIRTUAL_ENV
                uv sync --extra cu128
                UV_RC=$?
                if [ -n "$OLD_VIRTUAL_ENV" ]; then
                    export VIRTUAL_ENV="$OLD_VIRTUAL_ENV"
                fi
                exit "$UV_RC"
            )
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
