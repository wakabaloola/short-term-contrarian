# src/data_processing/process_sonia_raw.py

from src.utils.paths import RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR
from pathlib import Path
from typing import Union, Optional
import pandas as pd
import numpy as np
from datetime import datetime


def process_sonia_raw(
    read_filename: str = "sonia_raw.csv",
    read_dir: Union[str, Path] = RAW_DATA_DIR,
    read_date_format: str = "%d %b %y",
    read_column_date_name: str = "Date",
    read_column_name: str = "SONIA",
    write_filename: str = "sonia_interim.csv",
    write_dir: Union[str, Path] = INTERIM_DATA_DIR,
    write_date_format: str = "%Y-%m-%d",
    write_column_date_name: str = "Date",
    write_column_name: str = "SONIA",
    days_in_year: int = 252,
    dropna: bool = True
) -> None:
    """
    Reads a CSV file containing SONIA (Sterling Overnight Index Average) rates, 
    processes the data by converting annual rates to daily compounding rates, 
    and saves the processed data to a new CSV file.
    
    Args:
        read_filename (str): Name of the input CSV file containing raw SONIA data
        read_dir (Union[str, Path]): Directory path where the input file is located
        read_date_format (str): Date format string for parsing dates in the input file
        read_column_date_name (str): Name of the date column in the input file
        read_column_name (str): Name of the SONIA rate column in the input file
        write_filename (str): Name for the output processed CSV file
        write_dir (Union[str, Path]): Directory path where the output file will be saved
        write_date_format (str): Date format string for writing dates to the output file
        write_column_date_name (str): Name of the date column in the output file
        write_column_name (str): Name of the SONIA rate column in the output file
        days_in_year (int): Day count convention (e.g., 252 for business days, 365 for calendar days)
        dropna (bool): Whether to remove rows containing NaN values
    
    Returns:
        None
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the required columns are not found in the input file
        
    Example:
        >> example_data = pd.DataFrame({
        ..     'Date': ['01 Jan 23', '02 Jan 23', '03 Jan 23'],
        ..     'SONIA': [3.5, 3.6, 3.7]
        .. })
        >> example_data.to_csv('sonia_raw.csv')
        >> process_sonia_raw(
        ..     read_filename="sonia_raw.csv",
        ..     write_filename="sonia_processed.csv",
        ..     days_in_year=252
        .. )
        "The processed SONIA file has been created."
    """
    # Convert directory paths to Path objects if they're strings
    read_dir = Path(read_dir)
    write_dir = Path(write_dir)
    
    # Ensure input file exists
    read_filepath = read_dir / read_filename
    if not read_filepath.exists():
        raise FileNotFoundError(f"Input file not found: {read_filepath}")
    
    # Read the CSV file
    df = pd.read_csv(read_filepath)
    
    # Validate required columns exist
    if read_column_date_name not in df.columns or read_column_name not in df.columns:
        raise ValueError(f"Required columns {read_column_date_name} and/or {read_column_name} not found in input file")
    
    try:
        # Convert dates to datetime
        df[read_column_date_name] = pd.to_datetime(df[read_column_date_name], format=read_date_format)
        
        # Set index and name
        df.index = df[read_column_date_name]
        df.index = df.index.strftime(write_date_format)
        df = df[[read_column_name]]  # Keep only the rate column
        df.columns = [write_column_name]  # Rename the column
        
        # Convert annual rates to daily rates
        daily_rates = annual_to_daily_rates(
            df,
            days_in_year=days_in_year,
            dropna=dropna,
            convert_percentage_to_decimal=True
        )
        
        # Create output directory if it doesn't exist
        write_dir.mkdir(parents=True, exist_ok=True)
        
        # Save processed data
        write_filepath = write_dir / write_filename
        daily_rates.to_csv(write_filepath)
        
        if write_filepath.exists() and write_filepath.is_file():
            print(f"The processed {daily_rates.columns[0]} file has been created.")
        else:
            print(f"Error: The file {write_filepath} was not created successfully.")
            
    except Exception as e:
        raise RuntimeError(f"Error processing SONIA rates: {str(e)}")


def annual_to_daily_rates(
    annual_rates: pd.DataFrame,
    days_in_year: int,
    dropna: bool = True,
    convert_percentage_to_decimal: bool = True
) -> pd.DataFrame:
    """
    Converts annual interest rates to daily compounding rates.
    
    The conversion uses the formula: daily_rate = (1 + annual_rate)^(1/days_in_year) - 1
    
    Args:
        annual_rates (pd.DataFrame): DataFrame containing annual rates
        days_in_year (int): Number of days in the year (e.g., 252 for business days)
        dropna (bool): Whether to remove rows containing NaN values
        convert_percentage_to_decimal (bool): Whether to convert percentage values (e.g., 5.0) to decimals (0.05)
    
    Returns:
        pd.DataFrame: DataFrame containing the converted daily rates
        
    Raises:
        ValueError: If days_in_year is not positive
        
    Example:
        >> dates = pd.date_range('2023-01-01', '2023-01-03')
        >> df = pd.DataFrame({'Rate': [5.0, 4.5, 4.8]}, index=dates)
        >> annual_to_daily_rates(df, days_in_year=252)
                            Rate
        2023-01-01    0.000193
        2023-01-02    0.000174
        2023-01-03    0.000185
    """
    if days_in_year <= 0 or not isinstance(days_in_year, int):
        raise ValueError("days_in_year must be positive")
        
    # Create a copy to avoid modifying the input
    rates = annual_rates.copy()
    
    # Remove NaN values if specified
    if dropna:
        rates = rates.dropna()
    
    # Convert from percentage to decimal if specified
    if convert_percentage_to_decimal:
        rates = rates / 100
        
    # Convert to daily rates using the compound interest formula
    daily_rates = (1 + rates) ** (1 / days_in_year) - 1
    
    return daily_rates


if __name__ == "__main__":
    process_sonia_raw()
