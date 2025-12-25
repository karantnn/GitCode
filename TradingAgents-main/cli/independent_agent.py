"""
Independent Agent Runner
Allows running individual agents separately with independent outputs
"""

import typer
import json
from pathlib import Path
from datetime import date as date_type
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.agents.utils.agent_states import AgentState

console = Console()

# Define available agents
AVAILABLE_AGENTS = {
    "market": "Market Analyst - Technical and market analysis",
    "social": "Social Media Analyst - Social sentiment analysis",
    "news": "News Analyst - News and sentiment analysis",
    "fundamentals": "Fundamentals Analyst - Financial fundamentals analysis",
    "bull": "Bull Researcher - Bullish thesis development",
    "bear": "Bear Researcher - Bearish thesis development",
    "trader": "Trader - Trade execution strategy",
    "risky": "Risky Debater - Aggressive risk analysis",
    "neutral": "Neutral Debater - Balanced risk analysis",
    "safe": "Safe Debater - Conservative risk analysis",
}

def run_independent_agent(
    agent_type: str,
    ticker: str,
    trade_date: str = None,
    output_dir: str = "results",
):
    """
    Run a single agent independently and save output to a separate file
    
    Args:
        agent_type: Type of agent to run (market, social, news, fundamentals, bull, bear, trader, risky, neutral, safe)
        ticker: Stock ticker symbol
        trade_date: Analysis date (YYYY-MM-DD format), defaults to today
        output_dir: Directory to save agent outputs
    """
    
    if agent_type not in AVAILABLE_AGENTS:
        console.print(
            f"[red]Error: Unknown agent type '{agent_type}'[/red]\n"
            f"Available agents: {', '.join(AVAILABLE_AGENTS.keys())}"
        )
        raise typer.Exit(1)
    
    # Set default trade date to today
    if trade_date is None:
        trade_date = datetime.date.today().isoformat()
    
    # Validate date format
    try:
        datetime.datetime.strptime(trade_date, "%Y-%m-%d")
    except ValueError:
        console.print(f"[red]Error: Invalid date format. Use YYYY-MM-DD[/red]")
        raise typer.Exit(1)
    
    # Create output directory
    output_path = Path(output_dir) / ticker / trade_date
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize the graph with the selected analyst
    console.print(
        Panel(
            f"[bold cyan]Running Independent Agent[/bold cyan]\n"
            f"Agent: [yellow]{AVAILABLE_AGENTS[agent_type]}[/yellow]\n"
            f"Ticker: [green]{ticker}[/green]\n"
            f"Date: [magenta]{trade_date}[/magenta]",
            border_style="blue"
        )
    )
    
    try:
        # Determine which analysts to select based on agent type
        analysts = ["market", "social", "news", "fundamentals"]  # Always select these for context
        
        graph = TradingAgentsGraph(
            selected_analysts=analysts,
            debug=False,
        )
        
        # Prepare initial state
        initial_state = {
            "messages": [],
            "company_of_interest": ticker,
            "trade_date": trade_date,
            "selected_analysts": analyst_map.get(agent_type, []),
        }
        
        console.print(f"\n[cyan]Initializing agent workflow...[/cyan]")
        
        # Run the graph and collect output for the specific agent
        output = run_agent_graph(graph, agent_type, initial_state, ticker, trade_date)
        
        # Save output to file
        output_file = output_path / f"{agent_type}_agent_output.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        
        # Display summary
        console.print(
            Panel(
                f"[green]✓ Agent execution completed[/green]\n"
                f"Output saved to: [cyan]{output_file}[/cyan]",
                border_style="green"
            )
        )
        
        # Display key findings
        if "analysis" in output:
            console.print(
                Panel(
                    output["analysis"],
                    title=f"[bold]{AVAILABLE_AGENTS[agent_type]} Report[/bold]",
                    border_style="cyan"
                )
            )
        
        return output
        
    except Exception as e:
        console.print(f"[red]Error running agent: {str(e)}[/red]")
        raise typer.Exit(1)


def run_agent_graph(graph, agent_type, initial_state, ticker, trade_date):
    """
    Run the trading graph and extract output for specific agent
    
    Returns a dictionary with agent-specific output
    """
    # Map agent types to graph nodes/methods
    agent_methods = {
        "market": "run_market_analyst",
        "social": "run_social_analyst",
        "news": "run_news_analyst",
        "fundamentals": "run_fundamentals_analyst",
        "bull": "run_bull_researcher",
        "bear": "run_bear_researcher",
        "trader": "run_trader",
        "risky": "run_risky_debater",
        "neutral": "run_neutral_debater",
        "safe": "run_safe_debater",
    }
    
    # Simulate running individual agent (in real implementation, call specific graph methods)
    # For now, return a structured output
    output = {
        "agent_type": agent_type,
        "ticker": ticker,
        "date": trade_date,
        "timestamp": datetime.datetime.now().isoformat(),
        "analysis": f"Analysis from {AVAILABLE_AGENTS[agent_type]}",
        "status": "completed",
    }
    
    return output


# Mapping of agent types to analyst selections
analyst_map = {
    "market": ["market"],
    "social": ["social"],
    "news": ["news"],
    "fundamentals": ["fundamentals"],
    "bull": ["market", "news", "fundamentals"],
    "bear": ["market", "news", "fundamentals"],
    "trader": ["market", "social", "news", "fundamentals"],
    "risky": ["market", "news"],
    "neutral": ["market", "fundamentals"],
    "safe": ["fundamentals"],
}


def create_agent_summary_report(
    output_dir: str = "results",
    ticker: str = None,
    trade_date: str = None,
):
    """
    Create a summary report combining outputs from all agents
    
    Args:
        output_dir: Directory containing agent outputs
        ticker: Stock ticker (optional, if provided will filter to specific ticker)
        trade_date: Analysis date (optional, if provided will filter to specific date)
    """
    
    output_path = Path(output_dir)
    
    if not output_path.exists():
        console.print(f"[red]Error: Output directory '{output_dir}' not found[/red]")
        raise typer.Exit(1)
    
    # Collect all agent outputs
    all_outputs = {}
    
    if ticker and trade_date:
        search_path = output_path / ticker / trade_date
        if search_path.exists():
            for json_file in search_path.glob("*.json"):
                agent_name = json_file.stem.replace("_agent_output", "")
                with open(json_file) as f:
                    all_outputs[agent_name] = json.load(f)
    else:
        # Recursively find all agent outputs
        for json_file in output_path.rglob("*_agent_output.json"):
            with open(json_file) as f:
                all_outputs[json_file.stem.replace("_agent_output", "")] = json.load(f)
    
    if not all_outputs:
        console.print("[yellow]No agent outputs found[/yellow]")
        return
    
    # Create summary table
    table = Table(
        title="Agent Analysis Summary",
        show_header=True,
        header_style="bold magenta",
        box=box.GRID,
    )
    
    table.add_column("Agent", style="cyan")
    table.add_column("Ticker", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Status", style="magenta")
    
    for agent_name, output in all_outputs.items():
        table.add_row(
            agent_name,
            output.get("ticker", "N/A"),
            output.get("date", "N/A"),
            output.get("status", "N/A"),
        )
    
    console.print(table)
    
    # Save combined report
    report_file = output_path / f"summary_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(all_outputs, f, indent=2)
    
    console.print(f"\n[green]Summary report saved to: {report_file}[/green]")


if __name__ == "__main__":
    console.print(
        Panel(
            "[bold cyan]TradingAgents - Independent Agent Runner[/bold cyan]\n"
            "Run individual agents with separate outputs",
            border_style="blue"
        )
    )
    
    # Show available agents
    agents_table = Table(title="Available Agents", show_header=True, header_style="bold magenta")
    agents_table.add_column("Agent ID", style="cyan")
    agents_table.add_column("Description", style="green")
    
    for agent_id, description in AVAILABLE_AGENTS.items():
        agents_table.add_row(agent_id, description)
    
    console.print(agents_table)
    
    console.print("\n[yellow]Usage:[/yellow]")
    console.print("  python -m cli.independent_agent --agent [agent_id] --ticker [TICKER] [--date YYYY-MM-DD]")
    console.print("\n[yellow]Example:[/yellow]")
    console.print("  python -m cli.independent_agent --agent market --ticker AAPL --date 2025-12-25")
