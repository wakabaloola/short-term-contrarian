from pathlib import Path
import pandas as pd
from src.utils.paths import RAW_DATA_DIR

filepath = RAW_DATA_DIR / "sonia_raw.csv"

if filepath.exists():
    print("SONIA rates were manually downloaded from the Bank of England website:")
    print("https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")
    print(f"and stored in `{RAW_DATA_DIR}` with filename sonia_raw.csv")
    data = pd.read_csv(filepath)
else:
    raise FileNotFoundError(f"The file sonia_raw.csv was not found in the directory: {RAW_DATA_DIR}. It needs to be obtained manually from the Bank of England website: https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")

