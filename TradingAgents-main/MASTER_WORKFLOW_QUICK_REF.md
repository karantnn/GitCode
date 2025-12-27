# Master Workflow - Quick Reference

## One-Line Commands

```bash
# Default (market, fundamentals, news)
python scripts/master_workflow.py INTC

# With date
python scripts/master_workflow.py INTC 2025-12-25

# Market only
python scripts/master_workflow.py INTC 2025-12-25 -a market

# Multiple agents
python scripts/master_workflow.py INTC 2025-12-25 -a market fundamentals news

# All agents
python scripts/master_workflow.py INTC -a market fundamentals news bull bear neutral social trader risky safe
```

## What Happens

| Step | Input | Output | Time |
|------|-------|--------|------|
| 1. Validate | Check venv, CLI, converter | ✓/✗ | <1s |
| 2. Run agents | Selected agents | JSON files | 30-120s |
| 3. Discover JSON | Date folder | File list | <1s |
| 4. Convert | JSON files | .docx files | 30-60s |
| 5. Summary | All results | Report | <1s |

## Output Locations

```
results/TICKER/DATE/
├── *.json               ← Raw analysis files
└── reports/
    ├── *_analysis.docx  ← Individual documents
    └── Combined_Analysis.docx  ← All in one
```

## Agent Reference

| Agent | Description | Key Metrics |
|-------|-------------|-------------|
| `market` | Market analysis | Price, volume, trends |
| `fundamentals` | Financial data | P/E, earnings, ratios |
| `news` | News sentiment | Headlines, scores |
| `bull` | Bullish view | Upside potential |
| `bear` | Bearish view | Downside risk |
| `neutral` | Neutral analysis | Balanced view |
| `social` | Social media | Sentiment, trends |
| `trader` | Trading signals | Buy/sell points |
| `risky` | High risk | Aggressive strategy |
| `safe` | Low risk | Conservative strategy |

## Exit Status

```bash
# Success
echo $LASTEXITCODE  # 0

# Failure
echo $LASTEXITCODE  # 1
```

## Common Issues

| Problem | Solution |
|---------|----------|
| "venv not found" | Create: `python -m venv .venv` |
| "No JSON found" | Check agent output messages |
| "Word conversion failed" | Install: `pip install python-docx` |
| Takes too long | Run fewer agents: `-a market` |

## Time Estimates

- 1 agent: ~1 minute
- 3 agents: ~2 minutes
- 5 agents: ~3 minutes
- 10 agents: ~5 minutes

---

See [MASTER_WORKFLOW_GUIDE.md](MASTER_WORKFLOW_GUIDE.md) for complete documentation.
