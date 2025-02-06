import pandas as pd
from src.utils.paths import PROJECT_ROOT, RAW_DATA_DIR
from src.utils.parameters import ParameterEnvironment as PE
import yfinance as yf
import re

def get_tickers(env):
    s = Symbols(env)
    return s.get_symbols()


class Symbols:
    def __init__(self, env):
        if env == 'dow_jones_industrial_average':
            self.env = PE(
                name='DOW_JONES',
                url='https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
                table_number=2,
                SE='',
                column_key='Symbol',
                filename='symbols_dow_jones_industrial_average.csv'
            )
        elif env == 'snp_500':
            self.env = PE(
                name='SNP_500',
                url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                table_number=0,
                SE='',
                column_key='Symbol',
                filename='symbols_snp_500.csv'
            )
        elif env == 'nasdaq':
            self.env = PE(
                name='NASDAQ_100',
                url='https://en.wikipedia.org/wiki/Nasdaq-100',
                table_number=4,
                SE='',
                column_key='Symbol',
                filename='symbols_nasdaq.csv'
            )
        elif env == 'ftse_100':
            self.env = PE(
                name='FTSE_100',
                url='https://en.wikipedia.org/wiki/FTSE_100_Index',
                table_number=4,
                SE='LSE',
                column_key='Ticker',
                filename='symbols_ftse_100.csv'
            )
        elif env == 'ftse_250':
            self.env = PE(
                name='FTSE_250',
                url='https://en.wikipedia.org/wiki/FTSE_250_Index',
                table_number=3,
                SE='LSE',
                column_key='Ticker',
                filename='symbols_ftse_250.csv'
            )

        elif env == 'athex':
            self.env = PE(
                name='ATHEX',
                url='https://en.wikipedia.org/wiki/FTSE/Athex_Large_Cap',
                table_number=2,
                SE='ATHEX',
                column_key='Traded as',
                filename='symbols_athex.csv'
                )
        self.name = self.env.get('name')
        self.filename = self.env.get('filename')


    def ticker_exists(self, ticker_symbol: str) -> bool:
        ticker = yf.Ticker(ticker_symbol)
        if ticker.info:
            return True
        else:
            return False


    def get_symbols(self) -> list:
        """Returns a numpy array of a list of stock symbols or tickers (of type str) in the yfinance format corresponding to 'env' (short for 'environment'), and saves the entire table extracted from the provided url to a CSV file. The parameters are specified with `env`, an instance of `ParameterEnvironment` (imported as PE) from `parameters`. It is assumed that the following keys are defined: 'url', 'table_number', 'column_number', 'SE', 'filename'. 

        Examples of env:
        ================
        Get list of the Dow-Jones Industrial Average symbols, the FTSE 100 symbols, or the  FTSE/Athex Large Cap (the 25 largest companies on the Athens Stock Exchange) symbols from wikipedia. Save the corresponding table (in its original format) to a CSV.

        dow_jones_industrial_average = PE(
            url='https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
            table_number=2,
            SE='',
            column_key='Symbol',
            filename='symbols_dow_jones_industrial_average.csv'
        )

        ftse_100 = PE(
            url='https://en.wikipedia.org/wiki/FTSE_100_Index',
            table_number=4,
            SE='LSE',
            column_key='Ticker',
            filename='symbols_ftse_100.csv'
        )

        athex = PE(
            url='https://en.wikipedia.org/wiki/FTSE/Athex_Large_Cap',
            table_number=2,
            SE='ATHEX',
            column_key='Traded as',
            filename='symbols_athex.csv'
            )

        Dependencies:
        =============
        - yfinance (as yf)
        - pandas (as pd)
        - ParameterEnvironment (as PE) from parameters

        Caution:
        ========
        The wikipedia links and page contents change on a continual basis, and so the precise parameters in 'environment' (or some details in get_symbols()) might need to be corrected.
        """
        url = self.env.get('url')
        table_number = self.env.get('table_number')
        column_key = self.env.get('column_key')
        SE = self.env.get('SE')
        filename = self.env.get('filename')

        # Place the raw CSV data into the raw data directory
        filepath = RAW_DATA_DIR / filename

        tables = pd.read_html(url)
        table = tables[table_number]
        if filepath:
            table.to_csv(filepath, index=False)
        if SE == 'LSE' and type(table[column_key].values[0]) == str:
            # yf uses the convention that LSE tickers end in .L
            table[column_key] = table[column_key] + '.L'
        elif SE == 'ATHEX' and type(table[column_key].values[0]) == str:
            # yf uses the convention that ATHEX tickers end in .AT
            table[column_key] = table[column_key] + '.AT'
            table[column_key] = [x.replace('Athex:\xa0', '') for x in table[column_key].values]
        table[column_key] = [re.sub(r'(%5B\d+%5D|\[\d+\])', '', x) for x in table[column_key].values] # Remove potential superscripts
        stock_tickers = table[column_key].values
        
        stock_tickers = [ticker if self.ticker_exists(ticker) else 'invalid_ticker' for ticker in stock_tickers]
        return stock_tickers


if __name__ == "__main__":
    #s = Symbols('dow_jones_industrial_average')
    s = Symbols('nasdaq')
    #s = Symbols('snp_500')
    #s = Symbols('ftse_100')
    #s = Symbols('ftse_250')
    #s = Symbols('athex')
    symbols = s.get_symbols()
    print(symbols)
