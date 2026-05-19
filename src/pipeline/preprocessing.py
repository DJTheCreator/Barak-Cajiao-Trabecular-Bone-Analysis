# src/pipeline/preprocessing.py
from pathlib import Path
import pandas as pd
from scipy import integrate, stats
import numpy as np

from src.config.settings import QUICK_GRAPH, SKIPPED_TESTS, DEFAULT_SKIPPED_TESTS
from src.config.excel_format import USECOLS, SKIPROWS


def load_dataframes_from_files(*, path: Path):  # formerly createArrayFromFiles
    dataframes: list[pd.DataFrame] = []
    for file in path.iterdir():
        if any(test_name.upper() in file.name.upper() for test_name in SKIPPED_TESTS):
            continue
        if any(test_name.upper() in file.name.upper() for test_name in DEFAULT_SKIPPED_TESTS):
            continue
        df = pd.read_excel(file, usecols=USECOLS, skiprows=SKIPROWS)
        dataframes.append(df)
    return dataframes


# TODO Only integrate up to fracture point
def find_total_energy(dataframes: list[pd.DataFrame]):
    if QUICK_GRAPH:
        return 0
    energy_values = []
    for df in dataframes:
        energy_values.append(integrate.trapz(
            x=df.loc[:, 'Strain'],
            y=df.loc[:, 'Stress'])
        )
    return np.median(energy_values)


def find_ultimate_strength(dataframes: list[pd.DataFrame]):
    if QUICK_GRAPH:
        return 0
    max_values = []
    for df in dataframes:
        max_values.append(df.iloc[:, 0].max())
    return np.median(max_values)


# TODO Use 0.2% offset method
def find_youngs_modulus(dataframes: list[pd.DataFrame]):
    if QUICK_GRAPH:
        return 0
    window_width = .005
    step_size = .0001
    best_slopes = []
    all_best_window_bounds = [[], []]

    for df in dataframes:
        max_strain = df['Strain'].max(skipna=True)
        best_r2 = -1.0
        best_E = 0
        best_window_bounds = []

        for start_strain in np.arange(0, max_strain - window_width, step_size):
            end_strain = start_strain + window_width

            mask = (df['Strain'] >= start_strain) & (df['Strain'] <= end_strain)
            window_strain = df['Strain'][mask]
            window_stress = df['Stress'][mask]

            if len(window_strain) > 5:
                res = stats.linregress(window_strain, window_stress)

                current_r2 = res.rvalue ** 2
                current_E = res.slope

                if current_r2 > best_r2:
                    best_r2 = current_r2
                    best_E = current_E
                    best_window_bounds = [start_strain, end_strain]
        best_slopes.append(best_E)
        all_best_window_bounds[0].append(best_window_bounds[0])
        all_best_window_bounds[1].append(best_window_bounds[1])
    return [np.median(best_slopes), all_best_window_bounds]


def calculate_median_graph(dataframes: list[pd.DataFrame]):
    step_size = 1e-6
    max_strain = max(df['Strain'].max(skipna=True) for df in dataframes)
    strain_grid = np.arange(0.0, max_strain, step_size)

    interpolated_stress_values = []
    for df in dataframes:
        strain_values: pd.Series = df.loc[:, 'Strain']
        stress_values: pd.Series = df.loc[:, 'Stress']
        interpolated_stress = np.interp(strain_grid, strain_values, stress_values, right=0.0)
        interpolated_stress_values.append(interpolated_stress)
    median_stress = np.median(interpolated_stress_values, axis=0)
    median_dataframe = pd.DataFrame({
        "Strain": strain_grid,
        "Stress": median_stress
    })
    return median_dataframe
