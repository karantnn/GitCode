# Independent Agent Runner

This module allows you to run individual agents independently with separate outputs. Instead of running all agents in an orchestrated workflow, you can run specific agents and get isolated results.

## Features

- **Independent Execution**: Run individual agents without orchestration overhead
- **Separate Outputs**: Each agent generates its own analysis file
- **Flexible Analysis**: Choose which agents to run based on your analysis needs
- **Comparison Tools**: Compare results from different agents on the same stock
- **JSON Storage**: All results stored in organized JSON format by ticker and date

## Available Agents

### Analyst Team
- **market**: Market Analyst - Technical and market trend analysis
- **social**: Social Media Analyst - Social sentiment and social media analysis  
- **news**: News Analyst - News sentiment and news-based analysis
- **fundamentals**: Fundamentals Analyst - Financial fundamentals and ratio analysis

### Research Team
- **bull**: Bull Researcher - Bullish thesis and upside potential research
- **bear**: Bear Researcher - Bearish thesis and downside risk research

### Trading & Risk Management
- **trader**: Trader - Trade execution and strategy recommendations
- **risky**: Risky Debater - Aggressive/risky perspective on risk management
- **neutral**: Neutral Debater - Balanced perspective on risk management
- **safe**: Safe Debater - Conservative/safe perspective on risk management

## Usage

### List Available Agents

```bash
python -m cli.main agent list
```

Shows all available agents with descriptions.

### Run Individual Agent

#### Basic usage (today's date):
```bash
python -m cli.main agent run --agent market --ticker AAPL
```

#### With specific date:
```bash
python -m cli.main agent run --agent news --ticker MSFT --date 2025-12-25
```

#### Shorthand:
```bash
python -m cli.main agent run -a fundamentals -t NVDA -d 2025-12-24
```

#### With custom output directory:
```bash
python -m cli.main agent run --agent bull --ticker TSLA --output my_results
```

### Compare Agent Results

Compare outputs from all agents for a specific stock and date:

```bash
python -m cli.main agent compare --ticker AAPL --date 2025-12-25
```

Shorthand:
```bash
python -m cli.main agent compare -t MSFT -d 2025-12-24
```

## Output Structure

Results are organized by ticker and date:

```
results/
├── AAPL/
│   └── 2025-12-25/
│       ├── market_analysis_120530.json
│       ├── news_analysis_120545.json
│       ├── fundamentals_analysis_120600.json
│       └── bull_analysis_120615.json
├── MSFT/
│   └── 2025-12-24/
│       ├── market_analysis_140230.json
│       └── trader_analysis_140245.json
```

## Running Multiple Agents

### Sequential Execution

Run multiple agents one after another:

```bash
# Run all analyst agents
python -m cli.main agent run -a market -t AAPL
python -m cli.main agent run -a social -t AAPL
python -m cli.main agent run -a news -t AAPL
python -m cli.main agent run -a fundamentals -t AAPL

# Run research agents
python -m cli.main agent run -a bull -t AAPL
python -m cli.main agent run -a bear -t AAPL

# Run risk analysis
python -m cli.main agent run -a risky -t AAPL
python -m cli.main agent run -a neutral -t AAPL
python -m cli.main agent run -a safe -t AAPL
```

### Batch Script Example

Create a file `run_all_agents.bat`:

```batch
@echo off
setlocal enabledelayedexpansion

set TICKER=%1
set DATE=%2

if "%TICKER%"=="" (
    echo Usage: run_all_agents.bat TICKER [DATE]
    exit /b 1
)

if "%DATE%"=="" (
    for /f "tokens=*" %%A in ('powershell -Command "[datetime]::Today.ToString('yyyy-MM-dd')"') do (
        set DATE=%%A
    )
)

echo Running all agents for %TICKER% on %DATE%

REM Analyst team
call python -m cli.main agent run -a market -t %TICKER% -d %DATE%
call python -m cli.main agent run -a social -t %TICKER% -d %DATE%
call python -m cli.main agent run -a news -t %TICKER% -d %DATE%
call python -m cli.main agent run -a fundamentals -t %TICKER% -d %DATE%

REM Research team
call python -m cli.main agent run -a bull -t %TICKER% -d %DATE%
call python -m cli.main agent run -a bear -t %TICKER% -d %DATE%

REM Risk management
call python -m cli.main agent run -a risky -t %TICKER% -d %DATE%
call python -m cli.main agent run -a neutral -t %TICKER% -d %DATE%
call python -m cli.main agent run -a safe -t %TICKER% -d %DATE%

REM Trader synthesis
call python -m cli.main agent run -a trader -t %TICKER% -d %DATE%

REM Compare all results
call python -m cli.main agent compare -t %TICKER% -d %DATE%

echo All agents completed. Results saved in results\%TICKER%\%DATE%
```

Run with:
```bash
.\run_all_agents.bat AAPL 2025-12-25
```

## Output Format

Each agent generates a JSON file with the following structure:

```json
{
  "agent": "market",
  "agent_name": "Market Analyst",
  "ticker": "AAPL",
  "date": "2025-12-25",
  "timestamp": "2025-12-25T14:05:30.123456",
  "status": "completed",
  "analysis": "Detailed analysis text...",
  "recommendation": "BUY|HOLD|SELL",
  "confidence": "high|medium|low",
  "key_findings": [...],
  "technical_indicators": {...},
  "signals": {...}
}
```

## Advantages Over Orchestrated Analysis

### 1. **Modularity**
- Run agents independently without orchestration overhead
- Perfect for testing individual agent performance
- Easy to swap or upgrade specific agents

### 2. **Parallelization**
- Run multiple agents in parallel (manually or via scripting)
- Agents don't wait for each other
- Faster overall analysis for large portfolios

### 3. **Flexibility**
- Choose exactly which agents to run
- Skip expensive analyses if not needed
- Custom analysis combinations

### 4. **Debugging & Development**
- Isolate issues to specific agents
- Easier to test agent changes
- Clear input/output for each agent

### 5. **Cost Optimization**
- Skip agents you don't need
- Only pay for analyses you use
- Particularly useful for high-cost agents

## Integration with Orchestrated Analysis

The independent agent runner works alongside the main orchestrated analysis:

```bash
# Run focused individual analysis
python -m cli.main agent run -a market -t AAPL

# OR run full orchestrated analysis
python -m cli.main analyze
```

You can also combine outputs:
- Use independent agents for quick analysis
- Use orchestrated analysis for comprehensive decision-making
- Compare results from both approaches

## Performance Tips

### 1. **Parallel Execution** (Windows PowerShell)

```powershell
# Run multiple agents in parallel
$agents = @("market", "social", "news", "fundamentals")
$agents | ForEach-Object -Parallel {
    python -m cli.main agent run -a $_ -t AAPL
} -ThrottleLimit 4
```

### 2. **Batch Processing Multiple Tickers**

```powershell
$tickers = @("AAPL", "MSFT", "NVDA", "GOOGL")
foreach ($ticker in $tickers) {
    foreach ($agent in $agents) {
        python -m cli.main agent run -a $agent -t $ticker
    }
}
```

### 3. **Caching & Reuse**

Agent analyses are cached by date, so running the same agent twice in one day returns the same results instantly.

## Troubleshooting

### Issue: "Unknown agent: [agent_name]"
**Solution**: Check spelling and use `python -m cli.main agent list` to see available agents.

### Issue: "No analysis results found"
**Solution**: Make sure you've run at least one agent for the ticker/date combination before comparing.

### Issue: Agent times out
**Solution**: Some agents may take time on first run (data fetching). Subsequent runs use cached data.

## Advanced Usage

### Custom Analysis Workflow

```python
from cli.agents import agent_app, execute_agent, AGENTS
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Load graph
graph = TradingAgentsGraph(selected_analysts=["market", "news"])

# Run custom sequence
for agent in ["market", "bull", "trader"]:
    result = execute_agent(graph, agent, state, "AAPL", "2025-12-25")
    print(f"{AGENTS[agent]['name']}: {result['recommendation']}")
```

### Programmatic Comparison

```python
import json
from pathlib import Path

results_dir = Path("results/AAPL/2025-12-25")
analyses = {}

for json_file in results_dir.glob("*.json"):
    with open(json_file) as f:
        data = json.load(f)
        agent_name = data["agent"]
        analyses[agent_name] = data

# Compare recommendations
for agent, analysis in analyses.items():
    print(f"{agent}: {analysis['recommendation']} ({analysis['confidence']})")
```

## Next Steps

1. **Run your first agent**: `python -m cli.main agent run -a market -t AAPL`
2. **List available agents**: `python -m cli.main agent list`
3. **Compare multiple agents**: Run several agents, then use `compare` command
4. **Create batch scripts**: Automate running sets of agents for your portfolio
5. **Integrate into workflows**: Combine with orchestrated analysis for comprehensive coverage

---

For more help:
```bash
python -m cli.main agent --help
python -m cli.main agent run --help
python -m cli.main agent compare --help
```
