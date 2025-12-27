@echo off
REM TradingAgents - Independent Agent Runner
REM Run individual agents with separate outputs

setlocal enabledelayedexpansion

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else if exist "tradingagents\Scripts\activate.bat" (
    call "tradingagents\Scripts\activate.bat"
) else (
    echo Virtual environment not found at .venv\Scripts\activate.bat
    echo Creating a new virtual environment at .venv ...
    python -m venv .venv
    call ".venv\Scripts\activate.bat"
    pip install -r requirements.txt
)

REM Parse command line arguments
set TICKER=%1
set DATE=%2
set AGENT=%3

if "%TICKER%"=="" (
    echo.
    echo TradingAgents - Independent Agent Runner
    echo.
    echo Usage:
    echo   run_agents.bat TICKER [DATE] [AGENT]
    echo.
    echo Examples:
    echo   run_agents.bat AAPL                          (run all agents, today)
    echo   run_agents.bat MSFT 2025-12-25               (run all agents, specific date)
    echo   run_agents.bat NVDA 2025-12-25 market        (run single agent)
    echo.
    echo Available agents:
    echo   market, social, news, fundamentals, bull, bear, trader, risky, neutral, safe
    echo.
    pause
    exit /b 1
)

REM Set default date to today if not provided
if "%DATE%"=="" (
    for /f "tokens=*" %%A in ('powershell -Command "[datetime]::Today.ToString('yyyy-MM-dd')"') do (
        set DATE=%%A
    )
)

REM Run single agent if specified
if not "%AGENT%"=="" (
    echo.
    echo Running %AGENT% agent for %TICKER% on %DATE%
    echo.
    python -m cli.main agent run --agent %AGENT% --ticker %TICKER% --date %DATE%
    pause
    exit /b %ERRORLEVEL%
)

REM Run all agents if no agent specified
echo.
echo Running all agents for %TICKER% on %DATE%
echo.

set AGENTS=market social news fundamentals bull bear risky neutral safe trader

for %%A in (%AGENTS%) do (
    echo.
    echo [%%A] Starting...
    python -m cli.main agent run --agent %%A --ticker %TICKER% --date %DATE%
    if !ERRORLEVEL! neq 0 (
        echo [%%A] failed with error !ERRORLEVEL!
        REM Continue to next agent instead of exiting
    ) else (
        echo [%%A] completed successfully
    )
)

echo.
echo.
echo All agents completed!
echo Results saved in: results\%TICKER%\%DATE%
echo.
echo Comparing all results...
python -m cli.main agent compare --ticker %TICKER% --date %DATE%
echo.
pause
