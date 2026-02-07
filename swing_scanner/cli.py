#!/usr/bin/env python3
"""
CLI interface for Swing Trade Scanner
"""

import click
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

from .scanner import SwingScanner

init(autoreset=True)


@click.group()
def cli():
    """Swing Trade Scanner - Find S&P 500 trading opportunities"""
    pass


@cli.command()
@click.option('--max-stocks', default=50, help='Maximum stocks to scan')
@click.option('--output', '-o', default=None, help='Output file path')
@click.option('--min-confidence', default=70, help='Minimum confidence threshold')
def scan(max_stocks, output, min_confidence):
    """Run swing trade scan on S&P 500"""
    
    print(Fore.CYAN + "┌" + "─" * 78 + "┐")
    print(Fore.CYAN + "│" + Fore.YELLOW + "                    SWING TRADE SCANNER                     ".center(78) + Fore.CYAN + "│")
    print(Fore.CYAN + "│" + Fore.WHITE + f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ".center(78) + Fore.CYAN + "│")
    print(Fore.CYAN + "└" + "─" * 78 + "┘")
    print()
    
    scanner = SwingScanner()
    
    try:
        opportunities = scanner.scan_sp500(max_stocks=max_stocks)
        
        # Filter by confidence
        filtered = [o for o in opportunities if o['confidence'] >= min_confidence]
        
        if not filtered:
            print(Fore.YELLOW + "\n⚠️  No high-confidence opportunities found.")
            print(Fore.WHITE + "Try lowering confidence threshold or check market conditions.")
            return
        
        # Generate and display report
        report = scanner.generate_report(filtered)
        print("\n" + report)
        
        # Save results
        scanner.save_results(filtered, output)
        
        # Summary
        summary = scanner.get_summary(filtered)
        print(f"\n{Fore.GREEN}✅ Summary: {summary['total']} opportunities | "
              f"Avg Confidence: {summary['avg_confidence']}% | "
              f"Avg R/R: {summary['avg_risk_reward']}:1")
        
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️  Scan interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
def watch():
    """Run scanner every 4 hours and alert on new opportunities"""
    import schedule
    import time
    
    print(Fore.GREEN + "👁️  Watch mode started. Press Ctrl+C to stop.")
    print(Fore.CYAN + "⏰ Scanning every 4 hours...")
    
    def job():
        scanner = SwingScanner()
        opportunities = scanner.scan_sp500()
        
        if opportunities:
            print(Fore.GREEN + f"\n🚨 Found {len(opportunities)} new opportunities!")
            # TODO: Add notification logic
    
    schedule.every(4).hours.do(job)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Watch mode stopped.")


if __name__ == '__main__':
    cli()