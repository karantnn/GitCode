#!/usr/bin/env python3
"""
Display Python environment and configuration details used by VS Code.
Run with: python check_env.py
"""

import sys
import os
import platform
from pathlib import Path

def mask_key(k: str | None) -> str:
    """Mask sensitive API keys for safe display."""
    if not k:
        return "EMPTY"
    if len(k) <= 12:
        return k
    return f"{k[:8]}...{k[-4:]}"

def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def main():
    print_header("Python Environment & Configuration")
    
    # Python Version
    print(f"\n[Python Version]")
    print(f"  Version:     {sys.version}")
    print(f"  Executable:  {sys.executable}")
    print(f"  Prefix:      {sys.prefix}")
    print(f"  Platform:    {platform.platform()}")
    
    # Virtual Environment
    print(f"\n[Virtual Environment]")
    venv_active = os.environ.get('VIRTUAL_ENV')
    if venv_active:
        print(f"  Active:      Yes")
        print(f"  Path:        {venv_active}")
        print(f"  Prompt:      {os.environ.get('VIRTUAL_ENV_PROMPT', 'N/A')}")
    else:
        print(f"  Active:      No (global Python)")
    
    # Working Directory
    print(f"\n[Working Directory]")
    print(f"  Current:     {os.getcwd()}")
    cwd_files = [f for f in os.listdir('.') if f in ['.env', 'requirements.txt', '.venv', 'tradingagents']]
    if cwd_files:
        print(f"  Project Files Found: {', '.join(cwd_files)}")
    
    # API Keys (masked)
    print(f"\n[API Keys / Secrets]")
    keys = {
        'OPENAI_API_KEY': 'OpenAI',
        'ALPHA_VANTAGE_API_KEY': 'Alpha Vantage',
    }
    for env_var, label in keys.items():
        value = os.environ.get(env_var)
        masked = mask_key(value)
        print(f"  {label:20} ({env_var:25}): {masked}")
    
    # .env File Status
    print(f"\n[.env File]")
    env_file = Path('.env')
    if env_file.exists():
        print(f"  Exists:      Yes")
        print(f"  Size:        {env_file.stat().st_size} bytes")
        print(f"  Path:        {env_file.absolute()}")
        try:
            with open('.env', 'r') as f:
                lines = f.readlines()
                print(f"  Lines:       {len(lines)}")
                print(f"  Variables defined:")
                for line in lines:
                    if '=' in line and not line.strip().startswith('#'):
                        key = line.split('=')[0].strip()
                        print(f"    - {key}")
        except Exception as e:
            print(f"  Error reading: {e}")
    else:
        print(f"  Exists:      No")
    
    # Python Path
    print(f"\n[Python Path (sys.path)]")
    for i, path in enumerate(sys.path[:5], 1):
        print(f"  {i}. {path}")
    if len(sys.path) > 5:
        print(f"  ... and {len(sys.path) - 5} more paths")
    
    # Installed Packages (key ones)
    print(f"\n[Key Installed Packages]")
    packages = ['dotenv', 'typer', 'langchain', 'openai', 'yfinance']
    for pkg in packages:
        try:
            mod = __import__(pkg)
            version = getattr(mod, '__version__', 'unknown')
            location = getattr(mod, '__file__', 'unknown')
            print(f"  {pkg:20} v{version:10} @ {location}")
        except ImportError:
            print(f"  {pkg:20} NOT INSTALLED")
    
    # Environment Overview
    print(f"\n[Environment Variables Summary]")
    important_vars = [
        'PATH', 'PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV', 'VIRTUAL_ENV_PROMPT',
        'PYTHONDONTWRITEBYTECODE', 'PYTHONUNBUFFERED', 'OPENAI_API_KEY', 
        'ALPHA_VANTAGE_API_KEY'
    ]
    for var in important_vars:
        value = os.environ.get(var)
        if value:
            if var in ['OPENAI_API_KEY', 'ALPHA_VANTAGE_API_KEY']:
                display = mask_key(value)
            elif var == 'PATH':
                paths = value.split(os.pathsep)
                display = f"{len(paths)} paths (first: {paths[0][:50]}...)"
            else:
                display = value[:60] + ('...' if len(value) > 60 else '')
            print(f"  {var:30} = {display}")
    
    print(f"\n{'='*70}\n")

if __name__ == '__main__':
    main()
