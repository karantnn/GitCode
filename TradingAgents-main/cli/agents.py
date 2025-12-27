"""
Individual Agent Commands for TradingAgents CLI
Allows running individual agents with separate outputs
"""

import typer
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import os
from dotenv import load_dotenv, find_dotenv

# Robust .env loading for external prompts; override global env with project .env
def _load_env():
    load_dotenv(override=True)
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("ALPHA_VANTAGE_API_KEY"):
        project_root = Path(__file__).resolve().parent.parent
        env_path = project_root / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=True)
        else:
            found = find_dotenv(usecwd=False)
            if found:
                load_dotenv(found, override=True)

_load_env()

console = Console()

# Core graph and state imports (top-level for shared functions)
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.agents.utils.agent_states import AgentState
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.dataflows.config import set_config

# Analyst node factories (used by execute_agent)
from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.agents.analysts.social_media_analyst import (
    create_social_media_analyst,
)
from tradingagents.agents.analysts.news_analyst import create_news_analyst
from tradingagents.agents.analysts.fundamentals_analyst import (
    create_fundamentals_analyst,
)
from tradingagents.graph.conditional_logic import ConditionalLogic
from tradingagents.graph.propagation import Propagator
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from tradingagents.agents import create_msg_delete
from tradingagents.agents.utils.agent_utils import (
    get_stock_data,
    get_indicators,
    get_news,
    get_global_news,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
)

# Create app group for individual agent commands
agent_app = typer.Typer(
    help="Run individual agents with independent outputs"
)

# Define available agents with descriptions
AGENTS = {
    "market": {
        "name": "Market Analyst",
        "description": "Technical and market trend analysis",
        "color": "cyan"
    },
    "social": {
        "name": "Social Media Analyst",
        "description": "Social sentiment and social media analysis",
        "color": "yellow"
    },
    "news": {
        "name": "News Analyst",
        "description": "News sentiment and news-based analysis",
        "color": "green"
    },
    "fundamentals": {
        "name": "Fundamentals Analyst",
        "description": "Financial fundamentals and ratio analysis",
        "color": "magenta"
    },
    "bull": {
        "name": "Bull Researcher",
        "description": "Bullish thesis and upside potential research",
        "color": "green"
    },
    "bear": {
        "name": "Bear Researcher",
        "description": "Bearish thesis and downside risk research",
        "color": "red"
    },
    "trader": {
        "name": "Trader",
        "description": "Trade execution and strategy recommendations",
        "color": "blue"
    },
    "risky": {
        "name": "Risky Debater",
        "description": "Aggressive/risky perspective on risk management",
        "color": "red"
    },
    "neutral": {
        "name": "Neutral Debater",
        "description": "Balanced perspective on risk management",
        "color": "yellow"
    },
    "safe": {
        "name": "Safe Debater",
        "description": "Conservative/safe perspective on risk management",
        "color": "green"
    },
}


@agent_app.command()
def list():
    """List all available agents"""
    table = Table(
        title="Available Agents",
        show_header=True,
        header_style="bold magenta",
        box=box.SIMPLE_HEAD,
    )
    
    table.add_column("ID", style="cyan", width=15)
    table.add_column("Name", style="bold", width=25)
    table.add_column("Description", style="white", width=50)
    
    for agent_id, agent_info in AGENTS.items():
        table.add_row(
            agent_id,
            agent_info["name"],
            agent_info["description"]
        )
    
    console.print(table)


@agent_app.command()
def run(
    agent: str = typer.Option(
        ...,
        "--agent",
        "-a",
        help="Agent type (market, social, news, fundamentals, bull, bear, trader, risky, neutral, safe)",
        rich_help_panel="Agent Selection"
    ),
    ticker: str = typer.Option(
        ...,
        "--ticker",
        "-t",
        help="Stock ticker symbol (e.g., AAPL, MSFT, NVDA)",
        rich_help_panel="Stock Selection"
    ),
    date: str = typer.Option(
        None,
        "--date",
        "-d",
        help="Analysis date in YYYY-MM-DD format (defaults to today)",
        rich_help_panel="Analysis Settings"
    ),
    output_dir: str = typer.Option(
        "results",
        "--output",
        "-o",
        help="Output directory for agent results",
        rich_help_panel="Output Settings"
    ),
):
    """
    Run a single agent independently with separate output
    
    Examples:
        python -m cli.main agent run --agent market --ticker AAPL
        python -m cli.main agent run --agent news --ticker MSFT --date 2025-12-25
        python -m cli.main agent run -a fundamentals -t NVDA
    """
    
    # Validate agent
    if agent not in AGENTS:
        console.print(f"[red]✗ Unknown agent: {agent}[/red]")
        console.print(f"[yellow]Available agents: {', '.join(AGENTS.keys())}[/yellow]")
        raise typer.Exit(1)
    
    # Validate ticker
    if not ticker or len(ticker) == 0:
        console.print("[red]✗ Ticker is required[/red]")
        raise typer.Exit(1)
    
    agent_info = AGENTS[agent]
    color = agent_info["color"]
    
    # Set default date to today if not provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        console.print("[red]✗ Invalid date format. Use YYYY-MM-DD[/red]")
        raise typer.Exit(1)
    
    # Display start info
    console.print(
        Panel(
            f"[bold {color}]{agent_info['name']}[/bold {color}]\n"
            f"[cyan]Running independent agent analysis[/cyan]\n\n"
            f"[white]Ticker:[/white] [green]{ticker.upper()}[/green]\n"
            f"[white]Date:[/white]   [yellow]{date}[/yellow]",
            border_style=color,
            title="[bold]Individual Agent Run[/bold]",
        )
    )
    
    try:
        # Create output directory
        output_path = Path(output_dir) / ticker.upper() / date
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Import here to avoid circular imports
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.agents.utils.agent_states import AgentState
        from tradingagents.default_config import DEFAULT_CONFIG
        from tradingagents.dataflows.config import set_config

        # Analyst node factories
        from tradingagents.agents.analysts.market_analyst import create_market_analyst
        from tradingagents.agents.analysts.social_media_analyst import (
            create_social_media_analyst,
        )
        from tradingagents.agents.analysts.news_analyst import create_news_analyst
        from tradingagents.agents.analysts.fundamentals_analyst import (
            create_fundamentals_analyst,
        )
        
        # Initialize graph with all analysts for context
        console.print("[cyan]Initializing trading graph...[/cyan]")
        graph = TradingAgentsGraph(
            selected_analysts=["market", "social", "news", "fundamentals"],
            debug=False,
        )
        
        # Prepare initial state
        initial_state = AgentState(
            messages=[],
            company_of_interest=ticker.upper(),
            trade_date=date,
            selected_analysts=get_analysts_for_agent(agent),
        )
        
        console.print(f"[cyan]Running {agent_info['name']}...[/cyan]")
        
        # Execute the specific agent (simplified - in production would execute actual agent logic)
        result = execute_agent(graph, agent, initial_state, ticker.upper(), date)
        
        # Save results
        output_file = output_path / f"{agent}_analysis_{datetime.now().strftime('%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        # Display result
        console.print(
            Panel(
                f"[green]✓ Analysis completed successfully[/green]\n"
                f"[cyan]Output saved to:[/cyan]\n[yellow]{output_file}[/yellow]",
                border_style="green"
            )
        )
        
        # Display summary table
        summary_table = Table(title="Analysis Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Agent", agent_info["name"])
        summary_table.add_row("Ticker", ticker.upper())
        summary_table.add_row("Date", date)
        summary_table.add_row("Timestamp", result.get("timestamp", "N/A"))
        summary_table.add_row("Status", result.get("status", "N/A"))
        
        console.print(summary_table)
        
    except Exception as e:
        console.print(f"[red]✗ Error running agent: {str(e)}[/red]")
        raise typer.Exit(1)


@agent_app.command()
def compare(
    ticker: str = typer.Option(
        ...,
        "--ticker",
        "-t",
        help="Stock ticker symbol",
    ),
    date: str = typer.Option(
        None,
        "--date",
        "-d",
        help="Analysis date (YYYY-MM-DD format)",
    ),
    output_dir: str = typer.Option(
        "results",
        "--output",
        "-o",
        help="Output directory to search",
    ),
):
    """
    Compare outputs from all agents for a specific stock and date
    
    Examples:
        python -m cli.main agent compare --ticker AAPL
        python -m cli.main agent compare -t MSFT -d 2025-12-25
    """
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    output_path = Path(output_dir) / ticker.upper() / date
    
    if not output_path.exists():
        console.print(f"[yellow]No analysis results found for {ticker.upper()} on {date}[/yellow]")
        raise typer.Exit(1)
    
    # Collect all agent outputs
    results = {}
    for json_file in output_path.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
            agent_name = data.get("agent", "unknown")
            results[agent_name] = data
    
    if not results:
        console.print("[yellow]No agent analyses found[/yellow]")
        raise typer.Exit(1)
    
    # Display comparison
    console.print(
        Panel(
            f"[bold cyan]Agent Analysis Comparison[/bold cyan]\n"
            f"[white]Ticker:[/white] [green]{ticker.upper()}[/green]\n"
            f"[white]Date:[/white]   [yellow]{date}[/yellow]\n"
            f"[white]Agents:[/white] [magenta]{len(results)} analysis{'' if len(results) == 1 else 'es'}[/magenta]",
            border_style="blue"
        )
    )
    
    # Create comparison table
    table = Table(title="Agent Analysis Summary", show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAD)
    table.add_column("Agent", style="cyan", width=20)
    table.add_column("Description", style="green", width=40)
    table.add_column("Status", style="yellow", width=15)
    
    for agent_id, agent_info in AGENTS.items():
        status = "[green]✓ Completed[/green]" if agent_id in results else "[yellow]⊗ Not Run[/yellow]"
        table.add_row(agent_info["name"], agent_info["description"], status)
    
    console.print(table)


def get_analysts_for_agent(agent_type: str) -> list:
    """Determine which analysts are relevant for a given agent type"""
    analyst_mapping = {
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
    return analyst_mapping.get(agent_type, [])


def execute_agent(graph, agent_type: str, initial_state, ticker: str, date: str) -> dict:
    """Execute a specific agent and return results.

    Currently implements real execution for analyst agents (market, social, news,
    fundamentals) by invoking their node functions directly. Other agent types
    return a structured placeholder pending further iteration.
    """

    # Ensure config is set for data tools
    set_config(DEFAULT_CONFIG)

    llm = graph.quick_thinking_llm

    factory_map = {
        "market": create_market_analyst,
        "social": create_social_media_analyst,
        "news": create_news_analyst,
        "fundamentals": create_fundamentals_analyst,
    }

    result_obj = None
    analysis_text = None
    status = "completed"

    if agent_type in factory_map:
        # Build a minimal single-analyst graph to properly handle tool calls
        try:
            # Create nodes
            analyst_node = factory_map[agent_type](llm)
            clear_node = create_msg_delete()

            # Map tools per analyst
            tools_map = {
                "market": [get_stock_data, get_indicators],
                "social": [get_news],
                "news": [get_news, get_global_news],
                "fundamentals": [
                    get_fundamentals,
                    get_balance_sheet,
                    get_cashflow,
                    get_income_statement,
                ],
            }
            tool_node = ToolNode(tools_map[agent_type])

            # Build workflow
            workflow = StateGraph(AgentState)
            title = f"{agent_type.capitalize()} Analyst"
            workflow.add_node(title, analyst_node)
            workflow.add_node(f"Msg Clear {agent_type.capitalize()}", clear_node)
            workflow.add_node(f"tools_{agent_type}", tool_node)

            logic = ConditionalLogic()
            workflow.add_edge(START, title)
            workflow.add_conditional_edges(
                title,
                getattr(logic, f"should_continue_{agent_type}"),
                [f"tools_{agent_type}", f"Msg Clear {agent_type.capitalize()}"]
            )
            workflow.add_edge(f"tools_{agent_type}", title)
            workflow.add_edge(f"Msg Clear {agent_type.capitalize()}", END)

            graph_single = workflow.compile()

            # Prepare initial state
            propagator = Propagator()
            state = propagator.create_initial_state(ticker, date)
            args = propagator.get_graph_args()

            final_state = graph_single.invoke(state, **args)

            # Extract analysis from final state
            report_key_map = {
                "market": "market_report",
                "social": "sentiment_report",
                "news": "news_report",
                "fundamentals": "fundamentals_report",
            }
            analysis_text = final_state.get(report_key_map[agent_type])
        except Exception as e:
            status = "error"
            analysis_text = f"Agent execution failed: {e}"
    else:
        # Placeholder for non-analyst agents; will be implemented in next iteration
        analysis_text = f"Analysis from {AGENTS[agent_type]['name']} for {ticker} (placeholder)"

    return {
        "agent": agent_type,
        "agent_name": AGENTS[agent_type]["name"],
        "ticker": ticker,
        "date": date,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "analysis": analysis_text,
    }
