# config/exchanges.py
from src.data_acquisition.exchange import Exchange


DJIA = Exchange(
    name='DOW_JONES',
    url='https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average',
    table_number=2,
    pattern_and_replacement=(r'^([A-Z]{1,5})$', r'\1'),
    column_key='Symbol',
    filename='symbols_djia.csv'
)

SNP_500 = Exchange(
    name='SNP_500',
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
    table_number=0,
    pattern_and_replacement=(r'^([A-Z]{1,5})$', r'\1'),
    column_key='Symbol',
    filename='symbols_snp_500.csv'
)

NASDAQ_100 = Exchange(
    name='NASDAQ_100',
    url='https://en.wikipedia.org/wiki/Nasdaq-100',
    table_number=4,
    pattern_and_replacement=(r'^([A-Z]{1,5})$', r'\1'),
    column_key='Symbol',
    filename='symbols_nasdaq.csv'
)

FTSE_100 = Exchange(
    name='FTSE_100',
    url='https://en.wikipedia.org/wiki/FTSE_100_Index',
    table_number=4,
    pattern_and_replacement=(r'^([A-Z]{2,4})$', r'\1.L'),
    column_key='Ticker',
    filename='symbols_ftse_100.csv'
)

FTSE_250 = Exchange(
    name='FTSE_250',
    url='https://en.wikipedia.org/wiki/FTSE_250_Index',
    table_number=3,
    pattern_and_replacement=(r'^([A-Z]{2,4})$', r'\1.L'),
    column_key='Ticker',
    filename='symbols_ftse_250.csv'
)

ATHEX = Exchange(
    name='ATHEX',
    url='https://en.wikipedia.org/wiki/FTSE/Athex_Large_Cap',
    table_number=2,
    pattern_and_replacement=(r'^Athex:\s*(\w*)\s*(\[.+)?', r'\1.AT'),
    column_key='Traded as',
    filename='symbols_athex.csv'
)

CSI_100 = Exchange(
    name="CSI_100",
    url='https://en.wikipedia.org/wiki/CSI_100_Index',
    table_number=3,
    pattern_and_replacement=(
        r'^(SSE:\s*(\d+)|SZSE:\s*(\d+))$',
        lambda m: f"{m.group(2)}.SS" if m.group(2) else f"{m.group(3)}.SZ"
    ),
    column_key='Ticker',
    filename='symbols_csi_100.csv'
)

CSI_300 = Exchange(
    name='CSI_300',
    url='https://en.wikipedia.org/wiki/CSI_300_Index',
    table_number=3,
    pattern_and_replacement=(
        r'^(SSE:\s*(\d+)|SZSE:\s*(\d+))$',
        lambda m: f"{m.group(2)}.SS" if m.group(2) else f"{m.group(3)}.SZ"
    ),
    column_key='Ticker',
    filename='symbols_csi_300.csv'
)

# Create a dictionary for easy access to exchanges
EXCHANGES = {
    'DJIA': DJIA,
    'SNP_500': SNP_500,
    'NASDAQ_100': NASDAQ_100,
    'FTSE_100': FTSE_100,
    'FTSE_250': FTSE_250,
    'ATHEX': ATHEX,
    'CSI_100': CSI_100,
    'CSI_300': CSI_300
}
