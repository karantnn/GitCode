"""
Run All Agents Independently (Single Script)
- Executes selected agents separately
- Saves individual JSON outputs per agent
- Provides a simple summary at the end

Usage examples:
  python -m cli.run_all_agents --ticker INTC --date 2025-12-25
  python -m cli.run_all_agents --ticker AAPL --agents market news fundamentals
  python -m cli.run_all_agents --ticker MSFT --date 2025-12-25 --output results
"""

import json
import datetime
from pathlib import Path
from typing import List, Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from dotenv import load_dotenv
from rich.text import Text
from rich.rule import Rule
import textwrap

# Load environment variables
load_dotenv()

console = Console()
app = typer.Typer(help="Run all TradingAgents independently in one pass")

# Import shared CLI agent utilities
from cli.agents import (
    AGENTS,
    execute_agent,
)
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.agents.utils.agent_states import AgentState

DEFAULT_AGENT_ORDER = [
    "market",
    "social",
    "news",
    "fundamentals",
    "bull",
    "bear",
    "trader",
    "risky",
    "neutral",
    "safe",
]


@app.command()
def run(
    ticker: str = typer.Option(..., "--ticker", "-t", help="Stock ticker symbol"),
    date: Optional[str] = typer.Option(
        None,
        "--date",
        "-d",
        help="Analysis date (YYYY-MM-DD). Defaults to today",
    ),
    agents: Optional[str] = typer.Option(
        None,
        "--agents",
        help="Subset of agents to run (comma or space separated). Default runs all",
    ),
    output_dir: str = typer.Option(
        "results",
        "--output",
        "-o",
        help="Output directory",
    ),
):
    """
    Run selected agents independently and save outputs separately.
    """
    # Validate date
    if not date:
        date = datetime.date.today().isoformat()
    else:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid date format. Use YYYY-MM-DD[/red]")
            raise typer.Exit(1)

    ticker = ticker.upper()

    # Determine agent list
    if not agents or len(agents.strip()) == 0:
        agents_to_run = DEFAULT_AGENT_ORDER
    else:
        # split by comma or spaces
        tokens = [tok.strip() for tok in agents.replace(",", " ").split() if tok.strip()]
        bad = [a for a in tokens if a not in AGENTS]
        if bad:
            console.print(f"[red]Unknown agents: {', '.join(bad)}[/red]")
            console.print(f"[yellow]Available: {', '.join(AGENTS.keys())}[/yellow]")
            raise typer.Exit(1)
        agents_to_run = tokens

    # Header panel
    console.print(
        Panel(
            f"[bold cyan]TradingAgents - Batch Independent Run[/bold cyan]\n\n"
            f"Ticker: [green]{ticker}[/green]\n"
            f"Date:   [yellow]{date}[/yellow]\n"
            f"Agents: [magenta]{', '.join(agents_to_run)}[/magenta]",
            border_style="cyan",
        )
    )

    # Create graph once (analyst mini-graphs are built internally per agent)
    graph = TradingAgentsGraph(
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
    )

    # Prepare output directory
    out_root = Path(output_dir) / ticker / date
    out_root.mkdir(parents=True, exist_ok=True)

    # Execute agents sequentially
    results = []
    for agent in agents_to_run:
        console.print(f"[cyan]Running {AGENTS[agent]['name']}[/cyan]")
        try:
            # Minimal state (consumed internally per agent)
            initial_state = AgentState(
                messages=[],
                company_of_interest=ticker,
                trade_date=date,
                selected_analysts=[],
            )
            result = execute_agent(graph, agent, initial_state, ticker, date)

            fname = out_root / f"{agent}_analysis_{datetime.datetime.now().strftime('%H%M%S')}.json"
            with open(fname, "w") as f:
                json.dump(result, f, indent=2)

            console.print(
                Panel(
                    f"[green]✓ {AGENTS[agent]['name']} completed[/green]\n"
                    f"Saved: [yellow]{fname}[/yellow]",
                    border_style="green",
                )
            )
            results.append((agent, "completed", str(fname)))
        except Exception as e:
            console.print(f"[red]✗ {AGENTS[agent]['name']} failed: {e}[/red]")
            results.append((agent, "error", str(e)))

    # Summary table
    table = Table(title="Batch Summary", show_header=True, header_style="bold magenta", box=box.SIMPLE_HEAD)
    table.add_column("Agent", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Output / Error", style="yellow")

    for agent, status, info in results:
        label = AGENTS.get(agent, {}).get("name", agent)
        table.add_row(label, status, info)

    console.print(table)

    console.print(
        Panel(
            f"[bold green]Done[/bold green]\nOutputs: {out_root}",
            border_style="green",
        )
    )

    # Print Format-List style details for each generated JSON
    console.print(Rule("Details (Format-List)", style="cyan"))
    for agent, status, info in results:
        if status != "completed":
            continue
        try:
            data_path = Path(info)
            with open(data_path) as f:
                data = json.load(f)

            # Build Format-List style output
            lines = []
            # Preserve a consistent key order when available
            preferred_keys = [
                "agent",
                "agent_name",
                "ticker",
                "date",
                "timestamp",
                "status",
                "analysis",
            ]
            keys_emitted = set()
            for k in preferred_keys:
                if k in data:
                    val = data[k]
                    if isinstance(val, (dict, list)):
                        val_str = json.dumps(val, ensure_ascii=False)
                    else:
                        val_str = str(val)
                    # Wrap long values (especially analysis)
                    wrapped = textwrap.fill(val_str, width=100, subsequent_indent="             ")
                    lines.append(f"{k:<12} : {wrapped}")
                    keys_emitted.add(k)
            # Emit any remaining keys
            for k, v in data.items():
                if k in keys_emitted:
                    continue
                v_str = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
                wrapped = textwrap.fill(v_str, width=100, subsequent_indent="             ")
                lines.append(f"{k:<12} : {wrapped}")

            console.print(
                Panel(
                    Text("\n".join(lines)),
                    title=f"{AGENTS.get(agent, {}).get('name', agent)}",
                    border_style="cyan",
                )
            )
        except Exception as e:
            console.print(f"[red]Failed to display details for {agent}: {e}[/red]")


if __name__ == "__main__":
    app()
