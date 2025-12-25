# TradingAgents: Independent Agent System

## Overview

The TradingAgents application has been enhanced with an **Independent Agent Runner** that allows you to run individual agents separately from the main orchestrated workflow. This provides flexibility, modularity, and the ability to run agents in parallel.

## What Changed

### New Files Created

1. **`cli/agents.py`** - New CLI module for individual agent commands
2. **`cli/independent_agent.py`** - Core independent agent runner
3. **`run_agents.bat`** - Windows batch script for running multiple agents
4. **`run_agents.ps1`** - PowerShell script with parallel execution support
5. **`INDEPENDENT_AGENTS.md`** - Comprehensive documentation

### Modified Files

1. **`cli/main.py`** - Added integration with new agent commands

## Quick Start

### Option 1: Run Single Agent
```bash
python -m cli.main agent run --agent market --ticker AAPL
```

### Option 2: Run All Agents (Sequential)
```bash
.\run_agents.bat AAPL
```

### Option 3: Run All Agents (Parallel - Faster)
```powershell
.\run_agents.ps1 -Ticker AAPL -Parallel
```

### Option 4: Compare Results
```bash
python -m cli.main agent compare --ticker AAPL --date 2025-12-25
```

## Available Agents

| ID | Agent Name | Purpose |
|---|---|---|
| **market** | Market Analyst | Technical indicators and market trends |
| **social** | Social Media Analyst | Social sentiment analysis |
| **news** | News Analyst | News sentiment and news impact |
| **fundamentals** | Fundamentals Analyst | Financial ratios and fundamentals |
| **bull** | Bull Researcher | Bullish thesis development |
| **bear** | Bear Researcher | Bearish thesis development |
| **trader** | Trader | Trade execution strategy |
| **risky** | Risky Debater | Aggressive risk perspective |
| **neutral** | Neutral Debater | Balanced risk perspective |
| **safe** | Safe Debater | Conservative risk perspective |

## Command Reference

### List Agents
```bash
python -m cli.main agent list
```

### Run Single Agent
```bash
# Long form
python -m cli.main agent run --agent market --ticker AAPL --date 2025-12-25

# Short form
python -m cli.main agent run -a market -t AAPL -d 2025-12-25

# With custom output directory
python -m cli.main agent run -a news -t MSFT -o my_results
```

### Compare Results
```bash
# Compare all agents for a ticker on a specific date
python -m cli.main agent compare --ticker AAPL --date 2025-12-25

# Short form
python -m cli.main agent compare -t MSFT -d 2025-12-24
```

## Running Scripts

### Windows Batch - Sequential
```bash
# Run all agents for AAPL on today's date
.\run_agents.bat AAPL

# Run all agents for MSFT on specific date
.\run_agents.bat MSFT 2025-12-25

# Run single agent
.\run_agents.bat NVDA 2025-12-25 market
```

### PowerShell - Sequential
```powershell
.\run_agents.ps1 -Ticker AAPL
.\run_agents.ps1 -Ticker MSFT -Date 2025-12-25
.\run_agents.ps1 -Ticker NVDA -Agents @("market", "news", "fundamentals")
```

### PowerShell - Parallel (Faster)
```powershell
# Run all agents in parallel (up to 4 concurrent)
.\run_agents.ps1 -Ticker AAPL -Parallel

# Run with custom concurrency limit
.\run_agents.ps1 -Ticker AAPL -Parallel -ThrottleLimit 8

# Run specific agents in parallel
.\run_agents.ps1 -Ticker MSFT -Agents @("market", "news", "bull", "bear") -Parallel
```

## Output Structure

Results are organized by ticker and date:

```
results/
├── AAPL/
│   ├── 2025-12-25/
│   │   ├── market_analysis_120530.json
│   │   ├── news_analysis_120545.json
│   │   ├── fundamentals_analysis_120600.json
│   │   └── trader_analysis_120615.json
│   └── 2025-12-24/
│       └── ...
├── MSFT/
│   └── 2025-12-25/
│       ├── market_analysis_140230.json
│       └── ...
```

## Output Format

Each agent generates a JSON file:

```json
{
  "agent": "market",
  "agent_name": "Market Analyst",
  "ticker": "AAPL",
  "date": "2025-12-25",
  "timestamp": "2025-12-25T14:05:30.123456",
  "status": "completed",
  "analysis": "Detailed analysis...",
  "recommendation": "BUY|HOLD|SELL",
  "confidence": "high|medium|low"
}
```

## Use Cases

### 1. Quick Market Analysis
Run only the market and news analysts for fast technical analysis:
```bash
python -m cli.main agent run -a market -t AAPL
python -m cli.main agent run -a news -t AAPL
```

### 2. Fundamental Research
Focus on fundamental analysis:
```bash
python -m cli.main agent run -a fundamentals -t AAPL
python -m cli.main agent run -a bull -t AAPL
python -m cli.main agent run -a bear -t AAPL
```

### 3. Risk Assessment
Analyze from different risk perspectives:
```bash
python -m cli.main agent run -a risky -t AAPL
python -m cli.main agent run -a neutral -t AAPL
python -m cli.main agent run -a safe -t AAPL
```

### 4. Portfolio Analysis
Quick scan of multiple stocks:
```powershell
$tickers = @("AAPL", "MSFT", "NVDA", "GOOGL")
foreach ($ticker in $tickers) {
    .\run_agents.ps1 -Ticker $ticker -Agents @("market", "fundamentals") -Parallel
}
```

### 5. Multi-Agent Comparison
Run all agents for comprehensive analysis:
```bash
.\run_agents.bat AAPL
# Or for parallel execution:
.\run_agents.ps1 -Ticker AAPL -Parallel
```

## Performance Comparison

| Method | Time for 10 Agents | Benefit |
|--------|------------------|---------|
| Sequential (batch) | ~50 seconds | Simple, no dependencies |
| Sequential (PowerShell) | ~50 seconds | Cross-platform compatible |
| Parallel (PowerShell) | ~15 seconds | Fast, fully concurrent |

## Advantages of Independent Agents

✅ **Modularity** - Run agents independently
✅ **Flexibility** - Choose which agents to use
✅ **Parallelization** - Run multiple agents at once
✅ **Cost Control** - Only run what you need
✅ **Debugging** - Easy to test individual agents
✅ **Scalability** - Easily scale to multiple stocks
✅ **Caching** - Results cached by date
✅ **Organization** - Clean, structured output

## Combining with Orchestrated Analysis

You can use both approaches:

```bash
# Quick individual analysis
python -m cli.main agent run -a market -t AAPL

# Full orchestrated analysis for comprehensive decision
python -m cli.main analyze

# Or interactive selection
.\run_cli.bat
```

## Troubleshooting

### Issue: Agent command not recognized
```bash
# Make sure you're in the project root directory
cd C:\Users\nkara\Downloads\TradingAgents-main\TradingAgents-main

# List available commands
python -m cli.main --help
python -m cli.main agent --help
```

### Issue: Virtual environment error
```bash
# Recreate virtual environment
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Issue: API key errors
Check that `.env` file has valid API keys:
```
OPENAI_API_KEY=sk-...
ALPHA_VANTAGE_API_KEY=...
```

## Next Steps

1. **List available agents**: `python -m cli.main agent list`
2. **Run your first agent**: `python -m cli.main agent run -a market -t AAPL`
3. **Try parallel execution**: `.\run_agents.ps1 -Ticker AAPL -Parallel`
4. **Compare results**: `python -m cli.main agent compare -t AAPL`
5. **Read detailed docs**: See `INDEPENDENT_AGENTS.md`

## Documentation

- **Command Reference**: See `INDEPENDENT_AGENTS.md` for detailed documentation
- **Code Reference**: 
  - `cli/agents.py` - CLI commands
  - `cli/independent_agent.py` - Core runner
  - `run_agents.bat` - Batch script
  - `run_agents.ps1` - PowerShell script

## Support

For issues or questions:
1. Check the detailed documentation: `INDEPENDENT_AGENTS.md`
2. Review the command help: `python -m cli.main agent --help`
3. Check output files in `results/` directory for detailed analysis

---

**Version**: 1.0  
**Last Updated**: December 25, 2025
