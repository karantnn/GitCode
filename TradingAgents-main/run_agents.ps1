# TradingAgents - Independent Agent Runner (PowerShell)
# Run individual agents with separate outputs
# Supports parallel execution for faster analysis

param(
    [Parameter(Mandatory=$true)]
    [string]$Ticker,
    
    [Parameter(Mandatory=$false)]
    [string]$Date,
    
    [Parameter(Mandatory=$false)]
    [string[]]$Agents,
    
    [Parameter(Mandatory=$false)]
    [int]$ThrottleLimit = 4,
    
    [Parameter(Mandatory=$false)]
    [switch]$Parallel = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = "results"
)

# Set default date to today if not provided
if ([string]::IsNullOrEmpty($Date)) {
    $Date = (Get-Date).ToString("yyyy-MM-dd")
}

# Validate date format
try {
    [datetime]::ParseExact($Date, "yyyy-MM-dd", $null) | Out-Null
} catch {
    Write-Host "[ERROR] Invalid date format. Use yyyy-MM-dd" -ForegroundColor Red
    exit 1
}

# Default agents if not specified
if ($null -eq $Agents -or $Agents.Count -eq 0) {
    $Agents = @("market", "social", "news", "fundamentals", "bull", "bear", "trader", "risky", "neutral", "safe")
}

# Validate ticker
if ([string]::IsNullOrEmpty($Ticker)) {
    Write-Host "[ERROR] Ticker is required" -ForegroundColor Red
    exit 1
}

$Ticker = $Ticker.ToUpper()

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         TradingAgents - Independent Agent Runner               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ticker:  $Ticker" -ForegroundColor Green
Write-Host "Date:    $Date" -ForegroundColor Yellow
Write-Host "Agents:  $($Agents -join ', ')" -ForegroundColor Magenta
Write-Host "Parallel: $Parallel" -ForegroundColor Cyan
Write-Host "Output:  $OutputDir" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment if needed
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
} elseif (Test-Path ".\tradingagents\Scripts\Activate.ps1") {
    & ".\tradingagents\Scripts\Activate.ps1"
} else {
    Write-Host "[WARNING] Virtual environment not found. Make sure packages are installed." -ForegroundColor Yellow
}

# Function to run a single agent
function Run-Agent {
    param(
        [string]$Agent,
        [string]$Ticker,
        [string]$Date,
        [string]$OutputDir
    )
    
    $startTime = Get-Date
    Write-Host "[$Agent] Starting at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
    
    try {
        & python -m cli.main agent run `
            --agent $Agent `
            --ticker $Ticker `
            --date $Date `
            --output $OutputDir
        
        $duration = (Get-Date) - $startTime
        Write-Host "[$Agent] Completed in $([int]$duration.TotalSeconds)s" -ForegroundColor Green
        return @{
            Agent = $Agent
            Status = "Success"
            Duration = $duration
        }
    } catch {
        $duration = (Get-Date) - $startTime
        Write-Host "[$Agent] Failed after $([int]$duration.TotalSeconds)s: $_" -ForegroundColor Red
        return @{
            Agent = $Agent
            Status = "Failed"
            Duration = $duration
            Error = $_
        }
    }
}

# Run agents
$results = @()
$totalStart = Get-Date

if ($Parallel) {
    Write-Host "Running agents in PARALLEL mode (limit: $ThrottleLimit)..." -ForegroundColor Cyan
    Write-Host ""
    
    # Use ForEach-Object -Parallel for concurrent execution
    $results = $Agents | ForEach-Object -Parallel {
        $Agent = $_
        $outputObj = [pscustomobject]@{
            Agent = $Agent
            Ticker = $using:Ticker
            Date = $using:Date
            StartTime = Get-Date
        }
        
        Write-Host "[$Agent] Starting..." -ForegroundColor Cyan
        
        try {
            & python -m cli.main agent run `
                --agent $Agent `
                --ticker $using:Ticker `
                --date $using:Date `
                --output $using:OutputDir
            
            $outputObj | Add-Member -MemberType NoteProperty -Name Status -Value "Success"
        } catch {
            $outputObj | Add-Member -MemberType NoteProperty -Name Status -Value "Failed"
            $outputObj | Add-Member -MemberType NoteProperty -Name Error -Value $_.Exception.Message
        }
        
        $outputObj | Add-Member -MemberType NoteProperty -Name EndTime -Value (Get-Date)
        $outputObj
    } -ThrottleLimit $ThrottleLimit
} else {
    Write-Host "Running agents SEQUENTIALLY..." -ForegroundColor Cyan
    Write-Host ""
    
    foreach ($Agent in $Agents) {
        $result = Run-Agent -Agent $Agent -Ticker $Ticker -Date $Date -OutputDir $OutputDir
        $results += $result
    }
}

# Display summary
$totalDuration = (Get-Date) - $totalStart
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                      Analysis Summary                           ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Summary table
$summaryTable = $results | Select-Object @{Name="Agent"; Expression={$_.Agent}}, @{Name="Status"; Expression={$_.Status}} | Format-Table -AutoSize

Write-Host $summaryTable

$successCount = ($results | Where-Object {$_.Status -eq "Success"}).Count
$failureCount = ($results | Where-Object {$_.Status -eq "Failed"}).Count

Write-Host "Results:" -ForegroundColor Cyan
Write-Host "  Success: $successCount" -ForegroundColor Green
Write-Host "  Failed:  $failureCount" -ForegroundColor $(if ($failureCount -gt 0) { "Red" } else { "Green" })
Write-Host "  Total Time: $([int]$totalDuration.TotalSeconds)s" -ForegroundColor Yellow
Write-Host "  Output Directory: $OutputDir\$Ticker\$Date" -ForegroundColor Yellow
Write-Host ""

# Offer to show comparison
if ($successCount -gt 0) {
    Write-Host "Comparing results..." -ForegroundColor Cyan
    Write-Host ""
    & python -m cli.main agent compare --ticker $Ticker --date $Date --output $OutputDir
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
