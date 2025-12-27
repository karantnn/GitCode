# TradingAgents - JSON Conversion Tools

Complete solution for converting agent analysis JSON files to readable formats.

## 🚀 Quick Start

### Convert JSON to Word Document
```bash
# Single file
python scripts\json_to_word.py results\INTC\2025-12-25\analysis.json

# All files in directory
python scripts\json_to_word.py results\INTC\2025-12-25 -b

# Combine all into one document
python scripts\json_to_word.py results\INTC\2025-12-25 -b -c
```

### Convert JSON to Formatted Text
```bash
# View in list format
scripts\format_json.bat results\INTC\2025-12-25\analysis.json list

# View in table format
scripts\format_json.bat results\INTC\2025-12-25\analysis.json table

# View in tree format
scripts\format_json.bat results\INTC\2025-12-25\analysis.json tree
```

---

## 📚 Documentation
### Run Complete Workflow (Agents → JSON → Word Documents)
```bash
# Default: market, fundamentals, news agents
python scripts\master_workflow.py INTC

# Specific date and agents
python scripts\master_workflow.py INTC 2025-12-25 -a market fundamentals

# All available agents
python scripts\master_workflow.py INTC -a market fundamentals news bull bear neutral social trader risky safe
```

- **[CONVERSION_TOOLS_GUIDE.md](CONVERSION_TOOLS_GUIDE.md)** - Overview of both tools and use cases

### JSON to Word Converter
- **[JSON_TO_WORD_QUICK_REF.md](JSON_TO_WORD_QUICK_REF.md)** - Quick commands and examples
 **[MASTER_WORKFLOW_GUIDE.md](MASTER_WORKFLOW_GUIDE.md)** - Complete orchestration workflow guide
 **[MASTER_WORKFLOW_QUICK_REF.md](MASTER_WORKFLOW_QUICK_REF.md)** - Quick reference for master workflow

### JSON to Text Formatter
---


### 1. JSON to Word Converter
**Files**: 
- [scripts/json_to_word.py](scripts/json_to_word.py) - Main Python script
- [scripts/json_to_word.bat](scripts/json_to_word.bat) - Windows batch wrapper

**Features**:
- ✅ Single file or batch conversion
- ✅ Combine multiple analyses into one document
- ✅ Professional formatting with tables and styling
- ✅ Markdown header support
- ✅ Metadata display

**Output**: `.docx` Word documents (ready for sharing/printing)

---

### 2. JSON to Text Formatter
**Files**:
- [scripts/Format-JsonOutput.ps1](scripts/Format-JsonOutput.ps1) - PowerShell script
- [scripts/format_json.bat](scripts/format_json.bat) - Batch wrapper

**Features**:
- ✅ Three output formats (list, table, tree)
- ✅ Console or file output
- ✅ Value truncation for readability
- ✅ Nested structure support

**Output**: Formatted text (for terminals, sharing, quick viewing)

---

## 📖 Common Tasks

### View Analysis Quickly
```bash
scripts\format_json.bat results\INTC\2025-12-25\fundamentals.json table
```

### Create Professional Report
```bash
python scripts\json_to_word.py results\INTC\2025-12-25 -b -c
# Creates: Combined_Analysis.docx
```

### Archive Weekly Analyses
```bash
python scripts\json_to_word.py results\INTC\2025-12-25 -b -o archive/week52
```

### Compare Multiple Stocks
```bash
python scripts\json_to_word.py results\AAPL\2025-12-25 -b -c -o reports\AAPL.docx
python scripts\json_to_word.py results\MSFT\2025-12-25 -b -c -o reports\MSFT.docx
python scripts\json_to_word.py results\NVDA\2025-12-25 -b -c -o reports\NVDA.docx
```

---

## ✨ Features

| Feature | Text | Word |
|---------|------|------|
| Single file | ✓ | ✓ |
| Batch processing | - | ✓ |
| Combined output | - | ✓ |
| 3 formats | ✓ | - |
| Professional styling | - | ✓ |
| Metadata tables | ✓ | ✓ |
| File output | ✓ | ✓ |
| Console output | ✓ | - |

---

## 🔧 Installation

Required package (already installed):
```bash
pip install python-docx
```

---

## 📋 Command Reference

### Word Converter
```bash
# Basic
python scripts\json_to_word.py <input> [options]

# Options:
-b, --batch              Process all JSON in directory
-c, --combine            Combine all into single doc
-o, --output <dir>       Output directory/file
-p, --pattern <pat>      File pattern (default: *.json)
```

### Text Formatter
```bash
# Basic
scripts\format_json.bat <file> [format] [output]

# Formats: list, table, tree (default: list)
```

---

## 📊 Example Output

### Word Document Structure
```
┌──────────────────────────────────┐
│  Trading Agents Analysis Report  │
│  Agent Name - TICKER (DATE)      │
├──────────────────────────────────┤
│ Metadata                         │
│  • Agent: Fundamentals Analyst   │
│  • Ticker: INTC                  │
│  • Date: 2025-12-25              │
│  • Status: Completed             │
├──────────────────────────────────┤
│ Analysis Report                  │
│  ## Company Overview             │
│  Detailed analysis content...    │
│  ## Financial Metrics            │
│  More analysis...                │
└──────────────────────────────────┘
```

### Text Format Examples
```
LIST:
  agent : fundamentals
  ticker : INTC
  analysis : ## Report...

TABLE:
  +──────────────+─────────────────┐
  │ Property     │ Value           │
  ├──────────────┼─────────────────┤
  │ agent        │ fundamentals    │
  │ ticker       │ INTC            │

TREE:
  |-- agent : fundamentals
  |-- ticker : INTC
  +-- analysis : ## Report...
```

---

## 🎯 Use Cases

1. **Daily Reports** - Generate professional reports for stakeholders
2. **Stock Analysis** - Compare multiple stocks side-by-side
3. **Archive** - Save weekly/monthly analysis collections
4. **Quick View** - Inspect JSON content in terminal
5. **Distribution** - Email-ready Word documents
6. **Presentations** - Include in PowerPoint or reports

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Python not found | `.\.venv\Scripts\Activate.ps1` |
| python-docx not installed | `pip install python-docx` |
| File not found | Use absolute path or check spelling |
| Word won't open | Try different Word version or regenerate |
| Wrong format | Check output format flag (-b, -c, etc.) |

---

## 📞 Support

- **Full Documentation**: See CONVERSION_TOOLS_GUIDE.md
- **Quick Reference**: See JSON_TO_WORD_QUICK_REF.md
- **Script Help**: `python scripts\json_to_word.py -h`
- **Source Code**: Available in scripts/ directory

---

## 📝 File Organization

```
project/
├── scripts/
│   ├── json_to_word.py           ← Main converter
│   ├── json_to_word.bat          ← Batch wrapper
│   ├── Format-JsonOutput.ps1      ← Text formatter
│   └── format_json.bat           ← Text formatter wrapper
├── results/
│   └── TICKER/
│       └── DATE/
│           ├── *.json            ← Analysis outputs
│           └── reports/
│               ├── *.docx        ← Converted documents
│               └── Combined_Analysis.docx
├── CONVERSION_TOOLS_GUIDE.md      ← Start here!
├── JSON_TO_WORD_GUIDE.md
├── JSON_TO_WORD_QUICK_REF.md
└── FORMAT_JSON_GUIDE.md
```

---

## ✅ Status

- ✅ Python converter installed and tested
- ✅ Batch wrapper created and tested
- ✅ 49 documents successfully generated
- ✅ Combined document created
- ✅ Documentation complete
- ✅ Ready for production use

---

## Next Steps

1. **Review**: Read [CONVERSION_TOOLS_GUIDE.md](CONVERSION_TOOLS_GUIDE.md)
2. **Try**: Run a quick conversion: `python scripts\json_to_word.py results\INTC\2025-12-25 -b -c`
3. **Customize**: Edit scripts as needed for your workflow
4. **Integrate**: Add to your analysis pipeline
5. **Distribute**: Share Word documents with stakeholders

---

**Last Updated**: December 25, 2025
