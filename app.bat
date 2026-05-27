@echo off
setlocal
chcp 65001
cd /d "%~dp0"

if not exist "venv" (
    echo [ERROR] venv not found. Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate
echo [INFO] Starting VoiceDesignCloner...
echo [INFO] Browser will open automatically.
echo [INFO] Default URL: http://127.0.0.1:7860
echo [INFO] If 7860 is busy, the app will use the next free port.
python app.py
pause
