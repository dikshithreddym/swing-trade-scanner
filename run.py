#!/usr/bin/env python3
"""
Entry point for Swing Trade Scanner
"""

from swing_scanner import Scanner

if __name__ == '__main__':
    print("Spring Trade Scanner")
    print("=" * 80)
    
    # Initialize scanner
    scanner = Scanner()
    
    # Run scan
    opportunities = scanner.scan_sp500(max_stocks=50)
    
    # Generate report
    report = scanner.generate_report(opportunities)
    print(report)
    
    # Save results
    if opportunities:
        scanner.save_results(opportunities)