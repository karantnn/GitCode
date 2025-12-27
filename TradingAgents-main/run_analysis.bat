@echo off
REM Master Workflow - Windows Batch Wrapper
REM Complete Analysis: Run Agents ^> Read JSON ^> Create Word Documents
REM Usage: run_analysis.bat INTC [date] [agents]

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo.
    echo Usage: run_analysis.bat ^<ticker^> [date] [agents]
    echo.
    echo Arguments:
    echo   ticker    Stock symbol (required, e.g., AAPL, MSFT, INTC)
    echo   date      Analysis date (optional, format: YYYY-MM-DD, default: today)
    echo   agents    Agents to run (optional, comma-separated, default: market,fundamentals,news)
    echo.
    echo Examples:
    echo   run_analysis.bat INTC
    echo   run_analysis.bat INTC 2025-12-25
    echo   run_analysis.bat INTC 2025-12-25 market,fundamentals
    echo.
    exit /b 1
)

REM Get parameters
set TICKER=%~1
set DATE=%~2
set AGENTS=%~3

REM Set defaults
if "!DATE!"=="" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
    set DATE=!mydate!
)
if "!AGENTS!"=="" set AGENTS=market,fundamentals,news

REM Activate venv
cd /d "%~dp0"
call .\.venv\Scripts\Activate.ps1

REM Run master workflow
echo.
echo Starting analysis workflow...
echo Ticker: !TICKER! ^| Date: !DATE! ^| Agents: !AGENTS!
echo.

python scripts\master_workflow.py !TICKER! !DATE! -a !AGENTS:,= !

endlocal
