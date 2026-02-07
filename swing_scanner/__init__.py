"""
Swing Trade Scanner - S&P 500 Stock Opportunity Finder
"""

from .data_fetcher import DataFetcher
from .indicators import TechnicalIndicators
from .patterns import PatternDetector
from .scanner import SwingScanner

__version__ = "1.0.0"
__all__ = ['DataFetcher', 'TechnicalIndicators', 'PatternDetector', 'SwingScanner']