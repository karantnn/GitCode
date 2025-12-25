# JSON Formatter Scripts

Convert agent analysis JSON output files into readable text formats.

## Quick Start

### Using Batch Script (Windows CMD)
```batch
cd C:\Users\nkara\Downloads\TradingAgents-main\TradingAgents-main
scripts\format_json.bat results\INTC\2025-12-25\fundamentals_analysis_*.json table
```

### Using PowerShell
```powershell
cd C:\Users\nkara\Downloads\TradingAgents-main\TradingAgents-main
.\scripts\Format-JsonOutput.ps1 -JsonFile "results\INTC\2025-12-25\analysis.json" -Format list
```

## Available Scripts

### 1. **format_json.bat** (Windows Batch)
Lightweight wrapper script for Windows Command Prompt.

**Usage:**
```
format_json <json_file> [format] [output_file]
```

**Parameters:**
- `json_file` (required): Path to JSON file
- `format` (optional): Output format - `list`, `table`, or `tree` (default: `list`)
- `output_file` (optional): Save to file instead of console

**Examples:**
```batch
REM Display in table format
scripts\format_json.bat results\INTC\2025-12-25\fundamentals_analysis.json table

REM Save to file in list format
scripts\format_json.bat results\INTC\2025-12-25\news_analysis.json list output.txt

REM Display with tree format
scripts\format_json.bat results\INTC\2025-12-25\market_analysis.json tree
```

### 2. **Format-JsonOutput.ps1** (PowerShell)
Full-featured PowerShell script with detailed formatting options.

**Usage:**
```powershell
.\scripts\Format-JsonOutput.ps1 -JsonFile <path> -Format <format> [-OutputFile <path>]
```

**Parameters:**
- `-JsonFile` (required): Path to JSON file
- `-Format` (optional): `list` (default), `table`, or `tree`
- `-OutputFile` (optional): Save to file

**Examples:**
```powershell
# Display in list format (default)
.\scripts\Format-JsonOutput.ps1 -JsonFile "results\INTC\2025-12-25\fundamentals_analysis.json"

# Display in table format
.\scripts\Format-JsonOutput.ps1 -JsonFile "results\INTC\2025-12-25\fundamentals_analysis.json" -Format table

# Save to file
.\scripts\Format-JsonOutput.ps1 -JsonFile "results\INTC\2025-12-25\analysis.json" -Format list -OutputFile formatted_output.txt

# Tree format for hierarchical view
.\scripts\Format-JsonOutput.ps1 -JsonFile "results\INTC\2025-12-25\news_analysis.json" -Format tree
```

## Output Formats

### List Format (Default)
Detailed key-value listing with indented nested values.

```
========================================================================================
JSON Formatted Output
========================================================================================

agent : fundamentals
agent_name : Fundamentals Analyst
ticker : INTC
date : 2025-12-25
timestamp : 2025-12-25T12:15:11.086810
status : completed
analysis : ## Intel Corporation (INTC) Fundamental Analysis Report...
```

### Table Format
Aligned table with borders for easy scanning.

```
+------------+----------------------------------------------------------------------+
| Property   | Value                                                                  |
+------------+----------------------------------------------------------------------+
| agent      | fundamentals                                                           |
| agent_name | Fundamentals Analyst                                                   |
| ticker     | INTC                                                                   |
| timestamp  | 2025-12-25T12:15:11.086810                                             |
+------------+----------------------------------------------------------------------+
```

### Tree Format
Hierarchical display with branch indicators.

```
|-- agent : fundamentals
|-- agent_name : Fundamentals Analyst
|-- ticker : INTC
|-- date : 2025-12-25
|-- timestamp : 2025-12-25T12:15:11.086810
+-- analysis : ## Intel Corporation (INTC) Fundamental Analysis Report...
```

## Common Tasks

### Format all agent outputs for a specific stock and date
```batch
REM Format all analyses for INTC on 2025-12-25 in table format
for %%F in (results\INTC\2025-12-25\*.json) do (
    echo.
    echo === %%~nF ===
    scripts\format_json.bat "%%F" table
)
```

### Save formatted outputs to text files
```batch
REM Create formatted text versions of all JSON files
for %%F in (results\INTC\2025-12-25\*.json) do (
    scripts\format_json.bat "%%F" list "results\INTC\2025-12-25\%%~nF_formatted.txt"
)
```

### Compare different formats
```powershell
$file = "results\INTC\2025-12-25\fundamentals_analysis_121511.json"

Write-Host "=== LIST FORMAT ===" -ForegroundColor Cyan
.\scripts\Format-JsonOutput.ps1 -JsonFile $file -Format list

Write-Host "`n=== TABLE FORMAT ===" -ForegroundColor Cyan
.\scripts\Format-JsonOutput.ps1 -JsonFile $file -Format table

Write-Host "`n=== TREE FORMAT ===" -ForegroundColor Cyan
.\scripts\Format-JsonOutput.ps1 -JsonFile $file -Format tree
```

## Notes

- Long values are automatically truncated in table and tree formats
- Nested objects are displayed with indentation in list format
- Scripts handle both single and multiple-level nested JSON structures
- Output files are saved in UTF-8 encoding
- All scripts are compatible with Windows 10+

## Troubleshooting

### "JSON file not found" error
- Ensure the JSON file path is correct and relative to your project root
- Try using absolute path: `C:\Users\...\results\INTC\2025-12-25\analysis.json`

### PowerShell execution policy error
- The batch script automatically handles execution policy
- For manual PowerShell calls, use: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser`

### Output is truncated
- This is intentional for table/tree formats to fit terminal width
- Use list format for full output: `format_json <file> list`
- Or save to file for complete content: `format_json <file> list output.txt`
