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
echo [INFO] Browser will open automatically. If not, go to http://127.0.0.1:7860
python app.py
pause