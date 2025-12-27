# TradingAgents - Independent Agent Quick Reference

## Essential Commands

### List All Agents
```bash
python -m cli.main agent list
```

### Run Single Agent
```bash
python -m cli.main agent run -a <agent> -t <ticker> [-d <date>]
```

**Examples:**
```bash
python -m cli.main agent run -a market -t AAPL              # Today
python -m cli.main agent run -a news -t MSFT -d 2025-12-25  # Specific date
```

### Run All Agents (Sequential)
```bash
.\run_agents.bat <ticker> [<date>]
```

**Examples:**
```bash
.\run_agents.bat AAPL                    # All agents, today
.\run_agents.bat MSFT 2025-12-25         # All agents, specific date
```

### Run All Agents (Parallel - Faster)
```powershell
.\run_agents.ps1 -Ticker <ticker> [-Parallel] [-ThrottleLimit <n>]
```

**Examples:**
```powershell
.\run_agents.ps1 -Ticker AAPL -Parallel         # Parallel, default concurrency
.\run_agents.ps1 -Ticker MSFT -Parallel -ThrottleLimit 8  # Higher concurrency
```

### Compare Results
```bash
python -m cli.main agent compare -t <ticker> [-d <date>]
```

**Examples:**
```bash
python -m cli.main agent compare -t AAPL
python -m cli.main agent compare -t MSFT -d 2025-12-25
```

## Agent Types (Short Reference)

| Agent | Purpose |
|-------|---------|
| `market` | Technical analysis |
| `social` | Social sentiment |
| `news` | News sentiment |
| `fundamentals` | Financial analysis |
| `bull` | Bullish thesis |
| `bear` | Bearish thesis |
| `trader` | Trade strategy |
| `risky` | Aggressive perspective |
| `neutral` | Balanced perspective |
| `safe` | Conservative perspective |

## Common Workflows

### Quick Technical Check
```bash
python -m cli.main agent run -a market -t AAPL
```

### Fundamental Analysis
```bash
python -m cli.main agent run -a fundamentals -t AAPL
python -m cli.main agent run -a bull -t AAPL
python -m cli.main agent run -a bear -t AAPL
```

### Full Analysis (All 10 Agents)
```bash
# Sequential (slower, simpler)
.\run_agents.bat AAPL

# Parallel (faster)
.\run_agents.ps1 -Ticker AAPL -Parallel
```

### Risk Perspectives
```bash
python -m cli.main agent run -a risky -t AAPL
python -m cli.main agent run -a neutral -t AAPL
python -m cli.main agent run -a safe -t AAPL
```

### Multi-Stock Scan
```powershell
@("AAPL", "MSFT", "NVDA") | ForEach-Object {
    .\run_agents.ps1 -Ticker $_ -Agents @("market", "fundamentals") -Parallel
}
```

## Output Locations

```
results/
├── AAPL/2025-12-25/
│   ├── market_analysis_*.json
│   ├── news_analysis_*.json
│   ├── fundamentals_analysis_*.json
│   └── ...
```

## Common Issues

| Problem | Solution |
|---------|----------|
| Agent not found | `python -m cli.main agent list` to see available agents |
| Command not found | Make sure you're in project root directory |
| Virtual env error | Run `python -m venv .venv` then `.\.venv\Scripts\activate.bat` |
| API key error | Check `.env` file has OPENAI_API_KEY and ALPHA_VANTAGE_API_KEY |
| No results | Make sure agent completed (check console output) |

## Performance Tips

1. **Use parallel for speed**: `.\run_agents.ps1 -Ticker AAPL -Parallel`
2. **Use batch for simplicity**: `.\run_agents.bat AAPL`
3. **Run specific agents for speed**: Only run agents you need
4. **Cache results**: Same ticker/date runs use cached data

## Getting Help

```bash
python -m cli.main --help              # Main help
python -m cli.main agent --help        # Agent subcommand help
python -m cli.main agent run --help    # Run command help
python -m cli.main agent list          # List all agents
```

## Full Documentation

See `INDEPENDENT_AGENTS.md` for comprehensive documentation
See `AGENT_SYSTEM_GUIDE.md` for system overview

---

**Quick Start**: `python -m cli.main agent run -a market -t AAPL`
