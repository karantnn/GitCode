param(
    [Parameter(Mandatory=$true, HelpMessage="Path to the JSON file to format")]
    [string]$JsonFile,
    
    [Parameter(Mandatory=$false, HelpMessage="Output format: 'list', 'table', or 'tree' (default: list)")]
    [ValidateSet('list', 'table', 'tree')]
    [string]$Format = 'list',
    
    [Parameter(Mandatory=$false, HelpMessage="Output file path (optional; if not specified, outputs to console)")]
    [string]$OutputFile
)

# Validate input file exists
if (-not (Test-Path $JsonFile)) {
    Write-Host "Error: JSON file not found: $JsonFile" -ForegroundColor Red
    exit 1
}

# Read and parse JSON
try {
    $json = Get-Content $JsonFile -Raw | ConvertFrom-Json
    Write-Host "Loaded JSON file: $JsonFile" -ForegroundColor Green
} catch {
    Write-Host "Error parsing JSON: $_" -ForegroundColor Red
    exit 1
}

# Helper function to format nested objects recursively
function Format-JsonValue {
    param(
        [Parameter(ValueFromPipeline=$true)]
        $Value,
        
        [int]$Indent = 0
    )
    
    $indentStr = "  " * $Indent
    
    if ($Value -eq $null) {
        return "null"
    }
    elseif ($Value -is [bool]) {
        return $Value.ToString().ToLower()
    }
    elseif ($Value -is [int] -or $Value -is [double]) {
        return $Value.ToString()
    }
    elseif ($Value -is [string]) {
        # Truncate long strings
        if ($Value.Length -gt 200) {
            return $Value.Substring(0, 197) + "..."
        }
        return $Value
    }
    elseif ($Value -is [array]) {
        if ($Value.Count -eq 0) {
            return "[]"
        }
        $items = @()
        foreach ($item in $Value) {
            $formatted = Format-JsonValue $item ($Indent + 1)
            $items += "$indentStr  - $formatted"
        }
        return "`n" + ($items -join "`n")
    }
    elseif ($Value -is [pscustomobject]) {
        $props = @()
        foreach ($prop in $Value.PSObject.Properties) {
            $val = Format-JsonValue $prop.Value ($Indent + 1)
            if ($val.StartsWith("`n")) {
                $props += "$indentStr  $($prop.Name):`n$val"
            } else {
                $props += "$indentStr  $($prop.Name): $val"
            }
        }
        return "`n" + ($props -join "`n")
    }
    else {
        return $Value.ToString()
    }
}

# Format as List (detailed format)
function Format-AsListOutput {
    param($Data)
    
    $output = @()
    $separator = "=" * 88
    $output += $separator
    $output += "JSON Formatted Output"
    $output += $separator
    $output += ""
    
    foreach ($property in $Data.PSObject.Properties) {
        $name = $property.Name
        $value = $property.Value
        
        # Format value
        $formattedValue = Format-JsonValue $value 1
        
        if ($formattedValue.StartsWith("`n")) {
            $output += "$name :"
            $output += $formattedValue
        } else {
            # Truncate long single values
            if ($formattedValue.Length -gt 80) {
                $output += "$name : $($formattedValue.Substring(0, 77))..."
            } else {
                $output += "$name : $formattedValue"
            }
        }
        $output += ""
    }
    
    return $output -join "`n"
}

# Format as Table (key-value pairs)
function Format-AsTableOutput {
    param($Data)
    
    $table = @()
    $maxKeyLen = 0
    
    # First pass: find max key length
    foreach ($property in $Data.PSObject.Properties) {
        if ($property.Name.Length -gt $maxKeyLen) {
            $maxKeyLen = $property.Name.Length
        }
    }
    
    # Build table
    $topBorder = "+" + ("-" * ($maxKeyLen + 2)) + "+" + ("-" * 70) + "+"
    $sepBorder = "+" + ("-" * ($maxKeyLen + 2)) + "+" + ("-" * 70) + "+"
    $table += $topBorder
    
    $propHeader = "Property".PadRight($maxKeyLen)
    $valHeader = "Value".PadRight(70)
    $headerLine = "| " + $propHeader + " | " + $valHeader + " |"
    $table += $headerLine
    $table += $sepBorder
    
    foreach ($property in $Data.PSObject.Properties) {
        $name = $property.Name.PadRight($maxKeyLen)
        $value = Format-JsonValue $property.Value 0
        
        # Truncate value to fit
        if ($value.Length -gt 70) {
            $value = $value.Substring(0, 67) + "..."
        }
        $value = $value.PadRight(70)
        
        $line = "| " + $name + " | " + $value + " |"
        $table += $line
    }
    
    $table += $topBorder
    
    return $table -join "`n"
}

# Format as Tree (hierarchical)
function Format-AsTreeOutput {
    param($Data, [int]$Indent = 0)
    
    $output = @()
    $properties = @($Data.PSObject.Properties)
    $count = 0
    
    foreach ($property in $properties) {
        $count++
        $isLast = ($count -eq $properties.Count)
        $prefix = if ($isLast) { "+-- " } else { "|-- " }
        $continuation = if ($isLast) { "    " } else { "|   " }
        
        $indentStr = "  " * $Indent + $prefix
        $value = $property.Value
        
        if ($value -is [pscustomobject]) {
            $output += "$indentStr$($property.Name) :"
            $nestedOutput = Format-AsTreeOutput $value ($Indent + 1)
            foreach ($line in $nestedOutput) {
                $output += ("  " * $Indent + $continuation) + $line
            }
        } elseif ($value -is [array]) {
            $output += "$indentStr$($property.Name) : [$($value.Count) items]"
        } else {
            $formattedValue = Format-JsonValue $value 0
            if ($formattedValue.Length -gt 60) {
                $formattedValue = $formattedValue.Substring(0, 57) + "..."
            }
            $output += "$indentStr$($property.Name) : $formattedValue"
        }
    }
    
    return $output
}

# Generate output based on format
$result = switch ($Format) {
    'list' { Format-AsListOutput $json }
    'table' { Format-AsTableOutput $json }
    'tree' { Format-AsTreeOutput $json }
    default { Format-AsListOutput $json }
}

# Output results
if ($OutputFile) {
    $result | Out-File $OutputFile -Encoding UTF8
    Write-Host "Output written to: $OutputFile" -ForegroundColor Green
} else {
    Write-Host $result
}
