# Master Workflow Script Guide

Complete one-command analysis pipeline for trading agents.

## Quick Start

```bash
# Basic usage (default agents: market, fundamentals, news)
python scripts/master_workflow.py INTC

# Specify date
python scripts/master_workflow.py INTC 2025-12-25

# Choose specific agents
python scripts/master_workflow.py INTC 2025-12-25 -a market fundamentals

# Single agent analysis
python scripts/master_workflow.py INTC 2025-12-25 -a market
```

## What It Does

The master workflow orchestrates your entire analysis pipeline:

1. **VALIDATION** - Checks all required components
2. **RUNNING AGENTS** - Executes selected trading agents
3. **DISCOVERING JSON** - Finds all generated analysis files
4. **CONVERTING TO WORD** - Creates professional documents
5. **ANALYSIS COMPLETE** - Displays results summary

## Command Syntax

```
python master_workflow.py TICKER [DATE] [-a AGENTS...]
```

### Parameters

| Parameter | Description | Required | Default | Format |
|-----------|-------------|----------|---------|--------|
| `TICKER` | Stock symbol | Yes | - | uppercase, e.g., INTC, AAPL |
| `DATE` | Analysis date | No | Today | YYYY-MM-DD format |
| `-a, --agents` | Agents to run | No | market fundamentals news | Space-separated list |

### Available Agents

```
market              Market analysis
fundamentals       Fundamental analysis
news               News analysis
bull               Bull perspective
bear               Bear perspective
neutral            Neutral perspective
social             Social media analysis
trader             Trader perspective
risky              Risky portfolio
safe               Safe portfolio
```

## Examples

### Example 1: Complete Analysis (All Default Agents)
```bash
python scripts/master_workflow.py MSFT
```
- Ticker: MSFT
- Date: Today
- Agents: market, fundamentals, news
- Output: ~3 agents × 2 agents = ~6 documents + combined

### Example 2: Specific Date with Market Analysis Only
```bash
python scripts/master_workflow.py NVDA 2025-12-24 -a market
```
- Ticker: NVDA
- Date: December 24, 2025
- Agents: market only
- Output: 1 document + combined

### Example 3: Multiple Specific Agents
```bash
python scripts/master_workflow.py TSLA 2025-12-25 -a market fundamentals news bull bear
```
- Ticker: TSLA
- Date: December 25, 2025
- Agents: 5 different analyses
- Output: 5+ documents + combined

### Example 4: All Available Agents
```bash
python scripts/master_workflow.py AAPL -a market fundamentals news bull bear neutral social trader risky safe
```
- Ticker: AAPL
- Date: Today
- Agents: All 10 available agents
- Output: 10+ documents + combined

## Output Structure

Results are organized by ticker and date:

```
results/
  TICKER/
    DATE/
      *.json                   (raw analysis JSON files)
      reports/
        *_analysis_*.docx      (individual analysis documents)
        Combined_Analysis.docx (all analyses in one document)
```

### Example Output Path
```
results/INTC/2025-12-25/
├── market_analysis_115144.json
├── fundamentals_analysis_115848.json
├── news_analysis_115420.json
└── reports/
    ├── market_analysis_115144.docx
    ├── fundamentals_analysis_115848.docx
    ├── news_analysis_115420.docx
    └── Combined_Analysis.docx
```

## Output Messages

The script provides detailed progress reporting:

### Validation Phase
```
[+] Python venv found
[+] CLI module found
[+] JSON converter found
[+] Ticker: INTC
[+] Date: 2025-12-25
```

### Running Agents
```
[STEP 1] Running MARKET agent...
[+] MARKET agent completed

[STEP 2] Running FUNDAMENTALS agent...
[+] FUNDAMENTALS agent completed
```

### Discovering JSON
```
[+] Found 51 JSON file(s)
[*]   market_analysis_115144.json (1,208 bytes)
[*]   fundamentals_analysis_115848.json (4,669 bytes)
...
```

### Converting Documents
```
[*] Reports directory: results/INTC/2025-12-25/reports

[STEP 1] Converting individual JSON files...
[+] Converted 51 file(s) to Word

[STEP 2] Creating combined document...
[+] Created combined document (68.0 KB)
```

### Completion Summary
```
+- EXECUTION SUMMARY -------------------------------------------------+
| Stock Symbol:          INTC                           |
| Analysis Date:         2025-12-25                     |
| Agents Run:            2                              |
| JSON Files Created:    51                             |
| Word Documents:        52                             |
| Total Time:            1m 25s                        |
+- ------------------------------------------------------------------+
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Failure (validation or conversion error) |

Check exit code in scripts:
```bash
# PowerShell
python scripts/master_workflow.py INTC
if ($LASTEXITCODE -eq 0) { Write-Host "Success" }

# Batch
python scripts/master_workflow.py INTC
if %ERRORLEVEL% equ 0 (echo Success)

# Bash
python scripts/master_workflow.py INTC
if [ $? -eq 0 ]; then echo "Success"; fi
```

## Typical Execution Times

| Scenario | Expected Time |
|----------|---------------|
| Single agent (market only) | 30-45 seconds |
| Three agents (default) | 1-2 minutes |
| Five agents | 2-3 minutes |
| All 10 agents | 3-5 minutes |

Times vary based on:
- API response times
- JSON file sizes
- System performance
- Network connectivity

## Troubleshooting

### Error: "Python venv not found"
- Ensure `.venv` directory exists in project root
- Run `python -m venv .venv` to create it

### Error: "CLI module not found"
- Check that `cli/main.py` exists
- Verify project structure is intact

### Error: "No JSON files found"
- Agents may have failed to generate output
- Check agent output messages for errors
- Verify `results/TICKER/DATE/` directory exists

### Error: "Word conversion failed"
- Check that `scripts/json_to_word.py` exists
- Ensure `python-docx` is installed: `pip install python-docx`
- Verify JSON files are valid

### Agent Timeout
- Some agents may take longer than 120 seconds
- Check agent output messages
- Run specific agents individually if needed

### Unicode/Encoding Issues
- Script enforces UTF-8 output
- If errors persist, check Windows console encoding
- Try running in PowerShell 7+ for better UTF-8 support

## Integration Examples

### PowerShell Wrapper
```powershell
# run_analysis.ps1
param(
    [string]$Ticker = "INTC",
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    [string[]]$Agents = @("market", "fundamentals", "news")
)

& .\.venv\Scripts\python.exe scripts\master_workflow.py $Ticker $Date -a $Agents
```

Usage:
```powershell
.\scripts\run_analysis.ps1 -Ticker MSFT -Date 2025-12-25
```

### Batch Wrapper
```batch
@echo off
REM run_analysis.bat
set TICKER=%1
set DATE=%2
if "%TICKER%"=="" set TICKER=INTC
if "%DATE%"=="" for /f %%A in ('powershell get-date -format yyyy-MM-dd') do set DATE=%%A

.\.venv\Scripts\python.exe scripts\master_workflow.py %TICKER% %DATE%
```

Usage:
```batch
run_analysis.bat MSFT 2025-12-25
```

## Document Contents

Each generated `.docx` file includes:

### File Information Section
- Document type
- Stock ticker
- Analysis date
- File name

### Analysis Content
- Key metrics and findings
- Market insights (if market analysis)
- Financial metrics (if fundamental analysis)
- News summaries (if news analysis)
- Trading perspectives (if trader/bull/bear analysis)

### Combined Document
The `Combined_Analysis.docx` includes:
- All individual analyses merged
- Page breaks between analyses
- Single table of contents
- Consistent formatting throughout

## Performance Tips

1. **Run specific agents only** - Reduces execution time
   ```bash
   python scripts/master_workflow.py INTC -a market
   ```

2. **Batch multiple stocks** - Run analyses sequentially
   ```bash
   python scripts/master_workflow.py INTC 2025-12-25
   python scripts/master_workflow.py MSFT 2025-12-25
   python scripts/master_workflow.py NVDA 2025-12-25
   ```

3. **Combine results later** - Don't run all agents simultaneously
   - Each agent adds ~30-45 seconds
   - Combine results manually if needed

4. **Check results folder** - Documents appear as agents complete
   - Don't need to wait for 100% completion
   - Can open documents while workflow continues

## Advanced Usage

### Programmatic Execution
```python
from pathlib import Path
import subprocess
import sys

ticker = "INTC"
date = "2025-12-25"
agents = ["market", "fundamentals"]

result = subprocess.run([
    sys.executable,
    "scripts/master_workflow.py",
    ticker, date,
    "-a", *agents
])

if result.returncode == 0:
    print("Analysis completed successfully")
```

### Scheduled Analysis
Create Windows Task Scheduler task:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9:00 AM)
4. Set action: Run `run_analysis.bat` with parameters
5. Stock symbols analyzed automatically each day

### Multi-Stock Analysis Script
```bash
@echo off
for %%T in (INTC MSFT NVDA AAPL TSLA) do (
    echo.
    echo Analyzing %%T...
    .\.venv\Scripts\python.exe scripts\master_workflow.py %%T
)
echo All analyses complete
```

## Related Tools

- [FORMAT_JSON_GUIDE.md](FORMAT_JSON_GUIDE.md) - JSON text formatting
- [JSON_TO_WORD_GUIDE.md](JSON_TO_WORD_GUIDE.md) - Word document conversion details
- [CONVERSION_TOOLS_GUIDE.md](CONVERSION_TOOLS_GUIDE.md) - Complete toolkit reference

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Review agent output messages
3. Verify file paths and permissions
4. Check that all dependencies are installed

---

**Last Updated:** 2025-12-26  
**Master Workflow Version:** 1.0
