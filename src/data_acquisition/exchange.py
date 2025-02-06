# src/data_acquisition/exchange.py
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd
import re
import yfinance as yf
import time
from src.utils.logger import get_logger
from src.utils.paths import RAW_DATA_DIR

logger = get_logger(__name__)


@dataclass
class Exchange:
    """Represents a stock exchange and provides methods to fetch and validate stock symbols."""
    name: str
    url: str
    table_number: int
    pattern_and_replacement: Tuple[str]
    column_key: str
    filename: str

    def __post_init__(self):
        """Post-initialization hook for logging."""
        logger.debug(f'Initialised Exchange instance for {self.name}')


    def get_symbols(self) -> List[str]:
        """Download and process stock symbols for the exchange.
        
        Returns:
            List[str]: List of valid stock symbols
        """
        logger.info('Getting symbols')
        logger.debug('Specifying filepath directory/filename')
        filepath = RAW_DATA_DIR / self.filename
        
        # Check if the file already exists to avoid redundant downloads
        if filepath.exists():
            logger.debug(f"Filepath {filepath} exists")
            logger.info(f"Loading symbols from cached file: {filepath}")
            logger.debug('Attempting to pd.read_csv(filepath)')
            df = pd.read_csv(filepath)
            stock_tickers = df[self.column_key].tolist()
            return stock_tickers

        # If filename does not exist, download data using `url`
        try:
            logger.info(f"Fetching stock symbols from {self.url}")
            tables = pd.read_html(self.url)
        except ValueError as e:
            logger.error(f"Could not find table info at {self.url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching data from {self.url}: {e}")
            return []

        try:
            table = tables[self.table_number]
        except IndexError as e:
            logger.error(f"Table number {self.table_number} not found in {self.url}: {e}")
            return []

        # Process symbols
        logger.debug("Converting tickers' formats into the yf style")
        logger.debug(f"Available table keys = {table.keys}")
        pattern, repl = self.pattern_and_replacement
        table[self.column_key] = [re.sub(pattern, repl, x) for x in table[self.column_key].values]
        table[self.column_key] = [re.sub(r'(%5B\d+%5D|\[\d+\])', '', x) for x in table[self.column_key].values]
        self.table = table

        # Save raw table to CSV
        logger.info(f'Saving table to_csv({filepath}, index=False)')
        self.table.to_csv(filepath, index=False)

        # Validate tickers with yf
        logger.debug('Validating tickers with yf')
        stock_tickers = table[self.column_key].values
        stock_tickers = [ticker if self.ticker_exists(ticker) else 'invalid_ticker' for ticker in stock_tickers]
        return stock_tickers


    def ticker_exists(self, ticker_symbol: str) -> bool:
        """Check if a ticker symbol is recognized by yfinance.
        
        Args:
            ticker_symbol (str): The ticker symbol to validate

        Returns:
            bool: True if the ticker is valid, False otherwise
        """
        try:
            logger.debug('Checking if ticker symbol is recognised by yf')
            ticker = yf.Ticker(ticker_symbol)
            logger.debug(f'ticker.info = {ticker.info}')
            time.sleep(0.1)
            return bool(ticker.info)
        except Exception as e:
            logger.error(f'yf ticker check resulted in an exception: {e}')
            return False

