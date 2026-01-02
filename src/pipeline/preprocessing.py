# src/pipeline/preprocessing.py

from pathlib import Path
import pandas as pd
from src.config.excel_format import USECOLS, SKIPROWS


def load_dataframes_from_files(*, paths: Path):  # formerly createArrayFromFiles
    dataframes: list[pd.DataFrame] = []
    for file_path in paths:
        df = pd.read_excel(file_path, usecols=USECOLS, skiprows=SKIPROWS)
        dataframes.append(df)
    return dataframes
