# Master Workflow - PowerShell Wrapper
# Complete Trading Agents Analysis: Run Agents → Read JSON → Create Word Documents
# Usage: .\run_analysis.ps1 -Ticker INTC -Date 2025-12-25 -Agents market,fundamentals,news

param(
    [Parameter(Mandatory=$true, HelpMessage="Stock ticker symbol (e.g., AAPL, MSFT, INTC)")]
    [string]$Ticker,
    
    [Parameter(Mandatory=$false, HelpMessage="Analysis date in YYYY-MM-DD format (default: today)")]
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    
    [Parameter(Mandatory=$false, HelpMessage="Comma-separated agents to run (default: market,fundamentals,news)")]
    [string]$Agents = "market,fundamentals,news"
)

# Activate venv
$venvPath = "$(Split-Path -Parent $PSScriptRoot)\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
}

# Parse agents
$agentList = @()
if ($Agents -match ',') {
    $agentList = @($Agents -split ',\s*')
} else {
    $agentList = @($Agents)
}

# Build Python command
$pythonScript = Join-Path (Split-Path -Parent $PSScriptRoot) "scripts\master_workflow.py"
$args = @($Ticker, $Date, '-a') + $agentList

# Run
Write-Host ""
Write-Host "Starting analysis workflow..." -ForegroundColor Cyan
Write-Host "Ticker: $Ticker | Date: $Date | Agents: $Agents" -ForegroundColor Yellow
Write-Host ""

python $pythonScript @args
