# src/pipeline/preprocessing.py
from pathlib import Path
import pandas as pd
from numpy import median

from src.config.excel_format import USECOLS, SKIPROWS


def load_dataframes_from_files(*, path: Path):  # formerly createArrayFromFiles
    dataframes: list[pd.DataFrame] = []
    for file_path in path:
        df = pd.read_excel(file_path, usecols=USECOLS, skiprows=SKIPROWS)
        dataframes.append(df)
    return dataframes


def find_ultimate_strength(dataframes: list[pd.DataFrame]):
    max_values = []
    for df in dataframes:
        max_values.append(df.iloc[:, 0].max())
    return median(max_values)


def find_youngs_modulus(dataframes: list[pd.DataFrame]):
    return 0
