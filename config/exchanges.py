# config/exchanges.py
from src.data_acquisition.exchange import Exchange


DJIA = Exchange(
    name='DOW_JONES',
    url='https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
    table_number=2,
    yf_ticker_extension='',
    column_key='Symbol',
    filename='symbols_djia.csv'
)

SNP_500 = Exchange(
    name='SNP_500',
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
    table_number=0,
    yf_ticker_extension='',
    column_key='Symbol',
    filename='symbols_snp_500.csv'
)

NASDAQ_100 = Exchange(
    name='NASDAQ_100',
    url='https://en.wikipedia.org/wiki/Nasdaq-100',
    table_number=4,
    yf_ticker_extension='',
    column_key='Symbol',
    filename='symbols_nasdaq.csv'
)

FTSE_100 = Exchange(
    name='FTSE_100',
    url='https://en.wikipedia.org/wiki/FTSE_100_Index',
    table_number=4,
    yf_ticker_extension='.L',
    column_key='Ticker',
    filename='symbols_ftse_100.csv'
)

FTSE_250 = Exchange(
    name='FTSE_250',
    url='https://en.wikipedia.org/wiki/FTSE_250_Index',
    table_number=3,
    yf_ticker_extension='.L',
    column_key='Ticker',
    filename='symbols_ftse_250.csv'
)

ATHEX = Exchange(
    name='ATHEX',
    url='https://en.wikipedia.org/wiki/FTSE/Athex_Large_Cap',
    table_number=2,
    yf_ticker_extension='.AT',
    column_key='Traded as',
    filename='symbols_athex.csv'
)

# Create a dictionary for easy access to exchanges
EXCHANGES = {
    'DJIA': DJIA,
    'SNP_500': SNP_500,
    'NASDAQ_100': NASDAQ_100,
    'FTSE_100': FTSE_100,
    'FTSE_250': FTSE_250,
    'ATHEX': ATHEX
}
