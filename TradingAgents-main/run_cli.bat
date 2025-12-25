@echo off
rem Run the TradingAgents CLI as a module from the project root
@echo off
rem Run the TradingAgents CLI as a module from the project root
rem Usage: run_cli.bat [-- args]

setlocal enabledelayedexpansion

rem Change to the script directory (project root)
cd /d "%~dp0"

rem Ensure Python is available
where python >nul 2>&1
if errorlevel 1 (
  echo Python executable not found on PATH. Please install Python and re-run this script.
  pause
  exit /b 1
)

rem If .venv exists, activate it; otherwise create it and install requirements (optional)
if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else (
  echo Virtual environment not found at .venv\Scripts\activate.bat
  echo Creating a new virtual environment at .venv ^(this may take a minute^)...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create virtual environment. Aborting.
    pause
    exit /b 1
  )
  call ".venv\Scripts\activate.bat"
  if exist requirements.txt (
    echo Installing project requirements from requirements.txt ^(this may take several minutes^)...
    pip install -r requirements.txt
  ) else (
    echo No requirements.txt found; skipping dependency installation.
  )
)

rem Run the CLI as a module and forward any arguments
python -m cli.main %*

endlocal
exit /b %ERRORLEVEL%
where python >nul 2>&1
