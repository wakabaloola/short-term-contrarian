import pandas as pd
from src.utils.paths import RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR
import numpy as np


def filename_to_series(filename: str, column_name: str, date_format: str='%d %b %y', read_dir="raw") -> pd.Series:   # alternative date_format='%Y-%m-%d'
    if read_dir == "raw":
        _read_dir = RAW_DATA_DIR
    elif read_dir == "interim":
        _read_dir = INTERIM_DATA_DIR
    elif read_dir == "processed":
        _read_dir = PROCESSED_DATA_DIR
    else:
        raise ValueError('The write directory must be one of "raw", "interim" or "processed".')
    # Create filepath specifying CSV location
    filepath = _read_dir / filename
    # Construct dataframe
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df["Date"], format=date_format)
    df.index = df["Date"]
    series = df[column_name]
    return series


def filter_series(*args: tuple[pd.Series]) -> tuple[pd.Series]:
    df = pd.concat(args, axis=1)
    df = df.dropna()
    filtered_tuple_of_series = tuple(pd.Series(df.iloc[:,i]) for i in range(df.shape[1]))
    return filtered_tuple_of_series


def save_series(series: pd.Series, filename: str, write_dir="interim") -> None:
    if write_dir not in ["raw", "interim", "processed"]:
        raise ValueError('The write directory must be one of "raw", "interim" or "processed".')
    # Specify the write directory (as defined in ./src/utils/paths.py)
    if write_dir == "interim":
        _write_dir = INTERIM_DATA_DIR
    if write_dir == "processed":
        _write_dir = PROCESSED_DATA_DIR
    if write_dir == "raw":
        _write_dir = RAW_DATA_DIR
    # If series is a pd.Series instance, write to CSV
    if isinstance(series, pd.Series):
        filepath = _write_dir / filename
        series.to_csv(filepath)


# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    sonia = filename_to_series(filename='sonia_raw.csv', column_name="SONIA", date_format='%d %b %y', read_dir="raw")
    save_series(sonia, filename="sonia_yf_dates.csv", write_dir="interim")
