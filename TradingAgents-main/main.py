import os
try:
    from dotenv import load_dotenv
except Exception as _dot_err:
    print("Missing required package 'python-dotenv'. Install with:")
    print("    pip install python-dotenv")
    raise SystemExit(1)

# Load environment variables from .env (safer than hardcoding)
load_dotenv()

# Print masked API key values in bold before use (ANSI bold; may not render everywhere)
def _mask_key(k: str | None) -> str:
    if not k:
        return "EMPTY"
    if len(k) <= 12:
        return k
    return f"{k[:8]}...{k[-4:]}"

BOLD = "\x1b[1m"
RESET = "\x1b[0m"
print(f"{BOLD}ALPHA_VANTAGE_API_KEY: {_mask_key(os.environ.get('ALPHA_VANTAGE_API_KEY'))}{RESET}")
print(f"{BOLD}OPENAI_API_KEY: {_mask_key(os.environ.get('OPENAI_API_KEY'))}{RESET}")

# Import TradingAgents after env is prepared; provide a helpful error
# if dependencies are missing so users know to install requirements.
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
except Exception as _e:
    print("Missing dependencies or import error.")
    print("Please install project requirements and ensure your venv is activated:")
    print("    pip install -r requirements.txt")
    print("Original import error:", repr(_e))
    raise SystemExit(1)

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"  # Use a different model
config["quick_think_llm"] = "gpt-4o-mini"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds

# Configure data vendors (default uses yfinance and alpha_vantage)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: yfinance, alpha_vantage, local
    "technical_indicators": "yfinance",      # Options: yfinance, alpha_vantage, local
    "fundamental_data": "alpha_vantage",     # Options: openai, alpha_vantage, local
    "news_data": "alpha_vantage",            # Options: openai, alpha_vantage, google, local
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
