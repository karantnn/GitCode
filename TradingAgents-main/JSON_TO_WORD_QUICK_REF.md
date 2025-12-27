# JSON to Word Converter - Quick Reference

Convert agent analysis JSON files to professional Word documents.

## Installation

```bash
# Already installed
pip install python-docx
```

## Quick Start

### Single File

```powershell
# Convert one JSON to Word
python scripts\json_to_word.py "results\INTC\2025-12-25\fundamentals_analysis.json"

# Creates: fundamentals_analysis.docx in same directory
```

### All Files in Directory

```powershell
# Convert all JSON files to Word
python scripts\json_to_word.py "results\INTC\2025-12-25" -b

# Creates: market_analysis.docx, fundamentals_analysis.docx, etc.
```

### Combine All Into One Document

```powershell
# Create single combined document with all analyses
python scripts\json_to_word.py "results\INTC\2025-12-25" -b -c

# Creates: Combined_Analysis.docx (all reports in one file)
```

### Save to Custom Location

```powershell
# Save individual documents to reports folder
python scripts\json_to_word.py "results\INTC\2025-12-25" -b -o "reports"

# Save combined document to reports folder
python scripts\json_to_word.py "results\INTC\2025-12-25" -b -c -o "reports"
```

## Command Formats

| Use Case | Command |
|----------|---------|
| Single file | `python scripts\json_to_word.py <file.json>` |
| Batch convert | `python scripts\json_to_word.py <directory> -b` |
| Batch + combine | `python scripts\json_to_word.py <directory> -b -c` |
| Custom output | `python scripts\json_to_word.py <input> -o <output>` |
| All options | `python scripts\json_to_word.py <dir> -b -c -o <out> -p "*.json"` |

## Flags

- `-b, --batch`: Process all JSON files in directory
- `-c, --combine`: Combine into single document
- `-o, --output`: Output file/directory path
- `-p, --pattern`: File pattern (default: `*.json`)
- `-h, --help`: Show help

## Document Contents

Each Word document includes:

1. **Title Section**
   - Report title
   - Agent name, ticker, date

2. **Metadata Table**
   - Agent type
   - Stock ticker
   - Analysis date
   - Execution timestamp
   - Status

3. **Analysis Details**
   - Formatted analysis text
   - Sections from markdown headers
   - Bullet points (if any)

4. **Footer**
   - Generation timestamp
   - Source JSON filename

## Real Examples

### Example 1: Single Stock Analysis

```powershell
# Convert all INTC analyses and combine
python scripts\json_to_word.py results\INTC\2025-12-25 -b -c -o reports

# Output: reports\Combined_Analysis.docx
# Contains: Market, News, Fundamentals, Bull, Bear, etc.
```

### Example 2: Compare Multiple Stocks

```powershell
# AAPL report
python scripts\json_to_word.py results\AAPL\2025-12-25 -b -c -o reports\AAPL.docx

# MSFT report
python scripts\json_to_word.py results\MSFT\2025-12-25 -b -c -o reports\MSFT.docx

# NVDA report
python scripts\json_to_word.py results\NVDA\2025-12-25 -b -c -o reports\NVDA.docx
```

### Example 3: Archive Daily Reports

```powershell
# Create reports folder with date
$date = Get-Date -Format "yyyy-MM-dd"
mkdir "archive\$date"

# Convert current analysis
python scripts\json_to_word.py "results\INTC\$date" -b -c -o "archive\$date"
```

## Output Locations

| Input | Output (default) |
|-------|------------------|
| `file.json` | Same directory: `file.docx` |
| `directory/ -b` | Same directory: `*_analysis.docx` |
| `directory/ -b -c` | Same directory: `Combined_Analysis.docx` |
| `file.json -o out.docx` | Custom location: `out.docx` |
| `dir/ -b -o reports` | `reports/market_analysis.docx`, etc. |

## Formatting Features

- **Professional layout**: Calibri font, proper spacing
- **Markdown support**: Headers converted to Word headings
- **Metadata tables**: Organized key-value display
- **Color accents**: Blue headers and gray table backgrounds
- **Page breaks**: Between analyses in combined documents
- **Text truncation**: Long values abbreviated with "..."

## File Size Reference

- Single analysis: ~37-40 KB
- Combined (50 analyses): ~67 KB

## Batch Processing

### Convert All Daily Analyses (Last 7 Days)

```powershell
$dates = (0..6) | ForEach-Object {
    (Get-Date).AddDays(-$_).ToString("yyyy-MM-dd")
}

foreach ($date in $dates) {
    $dir = "results\INTC\$date"
    if (Test-Path $dir) {
        python scripts\json_to_word.py $dir -b -c -o "archive\$date"
        echo "✓ Converted $date"
    }
}
```

### Convert Multiple Stocks Same Day

```powershell
$stocks = @("AAPL", "MSFT", "NVDA", "INTC")
$date = "2025-12-25"

foreach ($stock in $stocks) {
    $dir = "results\$stock\$date"
    if (Test-Path $dir) {
        python scripts\json_to_word.py $dir -b -c -o "reports\$stock.docx"
        echo "✓ Converted $stock"
    }
}
```

## Troubleshooting

### Python not found
```powershell
.\.venv\Scripts\Activate.ps1
```

### python-docx not installed
```powershell
.\.venv\Scripts\Activate.ps1
pip install python-docx
```

### File already exists
- Specify different output location with `-o`
- Or delete existing file before converting

### JSON syntax error
- Validate JSON with format_json.bat first
- Check JSON for missing quotes or commas

## See Also

- [JSON_TO_WORD_GUIDE.md](JSON_TO_WORD_GUIDE.md) - Full documentation
- [FORMAT_JSON_GUIDE.md](FORMAT_JSON_GUIDE.md) - JSON text formatter
- [scripts/json_to_word.py](scripts/json_to_word.py) - Python source code

## Python API

```python
from scripts.json_to_word import json_to_word, batch_json_to_word

# Single file
json_to_word("analysis.json", "output.docx")

# Batch
batch_json_to_word("results/INTC/2025-12-25", "reports", combine=True)
```
