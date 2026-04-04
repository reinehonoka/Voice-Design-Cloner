@echo off
setlocal
chcp 65001

cd /d "%~dp0"

echo.
echo ============================================
echo   VoiceDesignCloner - Setup
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.12.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create venv
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] venv already exists. Skipping.
)

call venv\Scripts\activate

REM Detect GPU and install PyTorch
echo.
echo [INFO] Checking GPU...
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo [INFO] No NVIDIA GPU detected. Installing CPU version of PyTorch.
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
) else (
    echo [INFO] NVIDIA GPU detected. Installing CUDA version of PyTorch.
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
)

REM Upgrade packaging tools first. Some deps still use legacy setup.py flows.
echo.
echo [INFO] Upgrading pip/setuptools/wheel...
pip install -U pip setuptools wheel

REM sox may import numpy during metadata generation, so install it before requirements.
echo.
echo [INFO] Installing numpy first...
pip install numpy

REM Install dependencies
echo.
echo [INFO] Installing dependencies...
pip install -r requirements.txt

REM faster-qwen3-tts (CUDA Graph acceleration, GPU only)
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo [INFO] No NVIDIA GPU detected. Skipping faster-qwen3-tts.
) else (
    echo [INFO] Installing faster-qwen3-tts...
    pip install faster-qwen3-tts
)

echo.
echo ============================================
echo   Setup complete! Run app.bat to start.
echo ============================================
pause
