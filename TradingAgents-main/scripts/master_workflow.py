#!/usr/bin/env python3
"""
Master Script: Complete Trading Agent Analysis Workflow
Orchestrates: Run Agents -> Read JSON -> Create Word Documents
Takes: Stock ticker and date, handles all processes with progress messages
"""

import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import argparse
import os


class AnalysisOrchestrator:
    """Orchestrates complete analysis workflow with progress reporting"""
    
    def __init__(self, ticker: str, date: str, agents: List[str] = None):
        self.ticker = ticker.upper()
        self.date = date
        self.agents = agents or ["market", "fundamentals", "news"]
        self.project_root = Path(__file__).resolve().parent.parent
        self.results_dir = self.project_root / "results" / self.ticker / self.date
        self.reports_dir = self.results_dir / "reports"
        self.json_files = []
        self.word_files = []
        self.start_time = None
        
        # Force UTF-8 output
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    def log_section(self, title: str, color: str = "cyan"):
        """Print formatted section header"""
        print(f"\n{'=' * 70}")
        print(f"  {title}")
        print(f"{'=' * 70}\n")
    
    def log_step(self, step_num: int, message: str):
        """Print step message"""
        print(f"[STEP {step_num}] {message}")
    
    def log_success(self, message: str):
        """Print success message"""
        print(f"[+] {message}")
    
    def log_info(self, message: str):
        """Print info message"""
        print(f"[*] {message}")
    
    def log_warning(self, message: str):
        """Print warning message"""
        print(f"[!] {message}")
    
    def log_error(self, message: str):
        """Print error message"""
        print(f"[X] {message}")
    
    def validate_setup(self) -> bool:
        """Validate setup before running"""
        self.log_section("VALIDATION")
        
        # Check venv
        venv_path = self.project_root / ".venv"
        if not venv_path.exists():
            self.log_error(f"Python venv not found at {venv_path}")
            return False
        self.log_success(f"Python venv found")
        
        # Check CLI module
        cli_path = self.project_root / "cli" / "main.py"
        if not cli_path.exists():
            self.log_error(f"CLI module not found at {cli_path}")
            return False
        self.log_success(f"CLI module found")
        
        # Check converter script
        converter_path = self.project_root / "scripts" / "json_to_word.py"
        if not converter_path.exists():
            self.log_error(f"JSON converter not found at {converter_path}")
            return False
        self.log_success(f"JSON converter found")
        
        # Check ticker and date format
        if not self.ticker or len(self.ticker) == 0:
            self.log_error("Invalid ticker symbol")
            return False
        self.log_success(f"Ticker: {self.ticker}")
        
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
            self.log_success(f"Date: {self.date}")
        except ValueError:
            self.log_error(f"Invalid date format. Use YYYY-MM-DD")
            return False
        
        return True
    
    def run_agents(self) -> bool:
        """Run all selected agents"""
        self.log_section("RUNNING AGENTS")
        self.log_info(f"Ticker: {self.ticker} | Date: {self.date}")
        self.log_info(f"Agents to run: {', '.join(self.agents)}\n")
        
        failed_agents = []
        
        for i, agent in enumerate(self.agents, 1):
            self.log_step(i, f"Running {agent.upper()} agent...")
            
            cmd = [
                sys.executable,
                "-m", "cli.main",
                "agent", "run",
                "-a", agent,
                "-t", self.ticker,
                "-d", self.date
            ]
            
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    encoding="utf-8",
                    errors="replace"
                )
                
                if result.returncode == 0:
                    self.log_success(f"{agent.upper()} agent completed")
                else:
                    self.log_warning(f"{agent.upper()} agent returned code {result.returncode}")
                    if result.stderr:
                        self.log_info(f"  Error: {result.stderr[:100]}")
                    failed_agents.append(agent)
            
            except subprocess.TimeoutExpired:
                self.log_error(f"{agent.upper()} agent timed out")
                failed_agents.append(agent)
            except Exception as e:
                self.log_error(f"{agent.upper()} agent failed: {str(e)}")
                failed_agents.append(agent)
            
            time.sleep(1)
        
        if failed_agents:
            self.log_warning(f"{len(failed_agents)} agent(s) failed: {', '.join(failed_agents)}")
        
        return len(failed_agents) < len(self.agents)
    
    def discover_json_files(self) -> bool:
        """Discover generated JSON files"""
        self.log_section("DISCOVERING JSON FILES")
        
        if not self.results_dir.exists():
            self.log_error(f"Results directory not found: {self.results_dir}")
            return False
        
        # Find all JSON files for this date
        self.json_files = sorted(self.results_dir.glob("*.json"))
        
        if not self.json_files:
            self.log_warning(f"No JSON files found in {self.results_dir}")
            return False
        
        self.log_success(f"Found {len(self.json_files)} JSON file(s)")
        for json_file in self.json_files:
            file_size = json_file.stat().st_size
            self.log_info(f"  {json_file.name} ({file_size:,} bytes)")
        
        return True
    
    def convert_to_word(self) -> bool:
        """Convert JSON files to Word documents"""
        self.log_section("CONVERTING TO WORD DOCUMENTS")
        
        # Create reports directory
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.log_info(f"Reports directory: {self.reports_dir}\n")
        
        # Convert individual files
        self.log_step(1, "Converting individual JSON files...")
        
        cmd = [
            sys.executable,
            str(self.project_root / "scripts" / "json_to_word.py"),
            str(self.results_dir),
            "-b",
            "-o", str(self.reports_dir)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8",
                errors="replace"
            )
            
            if result.returncode == 0:
                docx_files = [f for f in self.reports_dir.glob("*.docx") 
                             if f.name != "Combined_Analysis.docx"]
                self.log_success(f"Converted {len(docx_files)} file(s) to Word")
                self.word_files.extend(docx_files)
            else:
                self.log_error(f"Conversion failed: {result.stderr[:200]}")
                return False
        
        except Exception as e:
            self.log_error(f"Conversion error: {str(e)}")
            return False
        
        # Create combined document
        self.log_step(2, "Creating combined document...")
        
        cmd_combined = [
            sys.executable,
            str(self.project_root / "scripts" / "json_to_word.py"),
            str(self.results_dir),
            "-b", "-c",
            "-o", str(self.reports_dir)
        ]
        
        try:
            result = subprocess.run(
                cmd_combined,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8",
                errors="replace"
            )
            
            if result.returncode == 0:
                combined = self.reports_dir / "Combined_Analysis.docx"
                if combined.exists():
                    size_kb = combined.stat().st_size / 1024
                    self.log_success(f"Created combined document ({size_kb:.1f} KB)")
                    self.word_files.append(combined)
            else:
                self.log_warning(f"Combined document creation failed")
        
        except Exception as e:
            self.log_warning(f"Combined document error: {str(e)}")
        
        return len(self.word_files) > 0
    
    def generate_summary(self):
        """Display comprehensive summary"""
        self.log_section("ANALYSIS COMPLETE")
        
        elapsed = time.time() - self.start_time
        minutes, seconds = divmod(int(elapsed), 60)
        
        # Summary table
        print("+- EXECUTION SUMMARY " + "-" * 49 + "+")
        print(f"| Stock Symbol:          {self.ticker:<30} |")
        print(f"| Analysis Date:         {self.date:<30} |")
        print(f"| Agents Run:            {len(self.agents):<30} |")
        print(f"| JSON Files Created:    {len(self.json_files):<30} |")
        print(f"| Word Documents:        {len(self.word_files):<30} |")
        print(f"| Total Time:            {minutes}m {seconds}s{' ':<23} |")
        print("+- " + "-" * 66 + "+\n")
        
        # Output files
        self.log_info(f"JSON Files: {self.results_dir}")
        self.log_info(f"Word Docs:  {self.reports_dir}\n")
        
        # File details
        if self.word_files:
            self.log_info("CREATED DOCUMENTS:")
            for word_file in sorted(self.word_files):
                size_kb = word_file.stat().st_size / 1024
                print(f"  {word_file.name:<45} {size_kb:>8.1f} KB")
        
        print()
        self.log_success("WORKFLOW COMPLETED SUCCESSFULLY!")
        self.log_info("Open the reports folder to view your documents")
        print()
    
    def run(self) -> bool:
        """Execute complete workflow"""
        self.start_time = time.time()
        
        # Welcome
        print("\n" + "=" * 70)
        print("  TRADING AGENTS - COMPLETE ANALYSIS WORKFLOW")
        print("  Run Agents -> Read JSON -> Create Word Documents")
        print("=" * 70 + "\n")
        
        # Step 1: Validate
        if not self.validate_setup():
            self.log_error("Setup validation failed. Aborting.")
            return False
        
        # Step 2: Run agents
        if not self.run_agents():
            self.log_warning("Some agents failed, but continuing...")
        
        # Step 3: Discover JSON
        if not self.discover_json_files():
            self.log_error("No JSON files found. Cannot continue.")
            return False
        
        # Step 4: Convert to Word
        if not self.convert_to_word():
            self.log_error("Word conversion failed.")
            return False
        
        # Step 5: Summary
        self.generate_summary()
        
        return True


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Complete Trading Agents Analysis Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze INTC today with default agents
  python master_workflow.py INTC
  
  # Analyze specific date
  python master_workflow.py INTC 2025-12-25
  
  # Specify agents to run
  python master_workflow.py INTC 2025-12-25 -a market fundamentals news
  
  # Only market analysis
  python master_workflow.py INTC 2025-12-25 -a market
        """
    )
    
    parser.add_argument(
        'ticker',
        help='Stock ticker symbol (e.g., AAPL, MSFT, INTC)'
    )
    
    parser.add_argument(
        'date',
        nargs='?',
        default=datetime.now().strftime("%Y-%m-%d"),
        help='Analysis date in YYYY-MM-DD format (default: today)'
    )
    
    parser.add_argument(
        '-a', '--agents',
        nargs='+',
        default=['market', 'fundamentals', 'news'],
        help='Agents to run (default: market fundamentals news)'
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = AnalysisOrchestrator(args.ticker, args.date, args.agents)
    
    # Run workflow
    success = orchestrator.run()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
