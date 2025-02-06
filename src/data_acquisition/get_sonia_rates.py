# src/data_acquisition/get_sonia_rates.py
from src.utils.logger import get_logger
from pathlib import Path
import pandas as pd
from src.utils.paths import RAW_DATA_DIR

logger = get_logger(__name__)

filepath = RAW_DATA_DIR / "sonia_raw.csv"
logger.debug(f'Defining filepath {filepath}')


if filepath.exists():
    logger.debug('Checked that filepath exists')
    print("SONIA rates were manually downloaded from the Bank of England website:")
    print("https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")
    print(f"and stored in `{RAW_DATA_DIR}` with filename sonia_raw.csv")
    logger.debug('Trying to read filepath using pandas -> dataframe')
    data = pd.read_csv(filepath)
else:
    logger.error(f'Filepath {filepath} to not exist, raising a FileNotFoundError.')
    raise FileNotFoundError(f"The file sonia_raw.csv was not found in the directory: {RAW_DATA_DIR}. It needs to be obtained manually from the Bank of England website: https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")

logger.info('Printing SONIA.csv to stdout')
print(data)
