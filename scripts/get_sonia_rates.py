import os
from src.utils.paths import PROJECT_ROOT, RAW_DATA_DIR


if os.path.exists(f"{RAW_DATA_DIR}/SONIAa.csv"):
    print("SONIA rates were manually downloaded from the Bank of England website:")
    print("https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")
    print(f"and stored in `{RAW_DATA_DIR}` with filename SONIA.csv")
else:
    raise FileNotFoundError(f"The file SONIA.csv was not found in the directory: {RAW_DATA_DIR}. It needs to be obtained manually from the Bank of England website: https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp")

