@echo off
REM Format JSON Output - Batch Script
REM Usage: format_json <json_file> [format] [output_file]
REM Formats: list (default), table, tree

if "%1"=="" (
    echo Usage: format_json ^<json_file^> [format] [output_file]
    echo Formats: list, table, tree
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Format-JsonOutput.ps1" -JsonFile "%1" -Format "%2" -OutputFile "%3"
