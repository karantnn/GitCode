@echo off
REM Convert JSON to Word Documents - Batch Wrapper
REM Usage: json_to_word <input> [--batch] [--combine] [-o output]

if "%~1"=="" (
    echo Usage: json_to_word ^<input^> [--batch] [--combine] [-o output]
    exit /b 1
)

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%.."

REM Run Python script with all arguments
python scripts\json_to_word.py %*

