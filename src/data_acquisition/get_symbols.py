# src/data_acquisition/get_symbols.py
from src.utils.logger import get_logger
from src.utils.paths import RAW_DATA_DIR
from config.exchanges import EXCHANGES
import argparse
import pandas as pd
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import re
import yfinance as yf

logger = get_logger(__name__)


def get_all_symbols() -> Dict[str, List[str]]:
    """Get symbols for all configured exchanges.
    
    Returns:
        Dict[str, List[str]]: Dictionary mapping exchange names to their symbol lists
    """
    results = {}
    for name, exchange in EXCHANGES.items():
        logger.info(f"Fetching symbols for {name}")
        symbols = exchange.get_symbols()
        results[name] = symbols
    return results


def get_exchange_symbols(exchange_name: str) -> Optional[List[str]]:
    """Get symbols for a specific exchange.
    
    Args:
        exchange_name (str): Name of the exchange to fetch symbols from

    Returns:
        Optional[List[str]]: List of symbols if exchange exists, None otherwise
    """
    if exchange_name not in EXCHANGES:
        available = ", ".join(EXCHANGES.keys())
        logger.error(f"Exchange {exchange_name} not found. Available exchanges: {available}")
        return None
    
    exchange = EXCHANGES[exchange_name]
    return exchange.get_symbols()


def main():
    """Command-line interface for fetching stock symbols from various exchanges.
    
    This script provides functionality to download and cache stock symbols from different 
    exchanges. It can be used both as a command-line tool and as an importable module.
    
    Command-line Usage:
        1. Fetch symbols from a specific exchange:
           $ python src/data_acquisition/get_symbols.py -e DJIA
           
        2. Fetch symbols from all configured exchanges:
           $ python src/data_acquisition/get_symbols.py --all
           
        3. Display help and available options:
           $ python src/data_acquisition/get_symbols.py --help
    
    Python Usage:
        from src.data_acquisition.get_symbols import get_exchange_symbols, get_all_symbols
        
        # Get symbols for a specific exchange
        ftse_symbols = get_exchange_symbols('FTSE_100')
        
        # Get symbols for all exchanges
        all_symbols = get_all_symbols()
    
    Options:
        -e, --exchange  Specify a single exchange to fetch symbols from
        -a, --all      Fetch symbols from all configured exchanges
        -h, --help     Show help message and exit
    
    Note:
        Downloaded symbols are cached in the RAW_DATA_DIR. Subsequent runs will use 
        cached data unless the corresponding CSV files are deleted.
    """
    parser = argparse.ArgumentParser(description='Fetch stock symbols from various exchanges')
    parser.add_argument('--exchange', '-e', 
                      choices=list(EXCHANGES.keys()),
                      help='Specific exchange to fetch symbols from')
    parser.add_argument('--all', '-a',
                      action='store_true',
                      help='Fetch symbols from all exchanges')
    
    args = parser.parse_args()
    
    if args.all:
        results = get_all_symbols()
        for exchange_name, symbols in results.items():
            print(f"\n{exchange_name} symbols:")
            print(symbols)
    elif args.exchange:
        symbols = get_exchange_symbols(args.exchange)
        if symbols:
            print(f"\n{args.exchange} symbols:")
            print(symbols)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
