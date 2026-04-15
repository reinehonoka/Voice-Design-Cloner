@echo off
setlocal enabledelayedexpansion
chcp 65001
cd /d "%~dp0"

echo.
echo ============================================
echo   VoiceDesignCloner - Setup
echo ============================================
echo.

REM --- Python version selection ---
set PYTHON_CMD=

REM Try py launcher first
py --list >nul 2>&1
if errorlevel 1 goto :try_python

REM Look for a compatible version (3.12 preferred, then 3.11, 3.10)
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.12
    echo [INFO] Found compatible Python 3.12 via py launcher.
    goto :create_venv
)
py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.11
    echo [INFO] Found compatible Python 3.11 via py launcher.
    goto :create_venv
)
py -3.10 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.10
    echo [INFO] Found compatible Python 3.10 via py launcher.
    goto :create_venv
)

REM No compatible version found via py launcher -- warn and use default py
for /f "tokens=2" %%V in ('py --version 2^>^&1') do set PY_VER=%%V
echo [WARN] No Python 3.10-3.12 found. Detected: !PY_VER!
echo [WARN] This version is not officially supported and may cause errors.
echo.
set /p CONT=Continue anyway? (y/N):
if /i "!CONT!" neq "y" (
    echo Aborted.
    pause
    exit /b 1
)
set PYTHON_CMD=py
goto :create_venv

:try_python
REM Fallback: use plain python command
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10-3.12.
    echo https://www.python.org/downloads/release/python-3120/
    pause
    exit /b 1
)
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set PY_VER=%%V
for /f "tokens=1,2 delims=." %%A in ("!PY_VER!") do (
    set PY_MAJOR=%%A
    set PY_MINOR=%%B
)
if !PY_MINOR! GTR 12 (
    echo [WARN] Python !PY_VER! is not officially supported (recommended: 3.10-3.12).
    echo [WARN] You may encounter errors during setup or at runtime.
    echo.
    set /p CONT=Continue anyway? (y/N):
    if /i "!CONT!" neq "y" (
        echo Aborted.
        pause
        exit /b 1
    )
)
set PYTHON_CMD=python
echo [INFO] Using python: !PY_VER!

:create_venv
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
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
