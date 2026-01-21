# src/pipeline/run_pipeline.py
from src.config.generation_settings import Analysis, OrientationData
from src.pipeline.preprocessing import *
import src.config.paths as paths


def generate_graph(analysis: Analysis):
    printer, method, orientations = analysis.printer.get(), analysis.method.get(), analysis.orientations

    # The location of the files used for the graph based on user config (analysis)
    data_path = paths.PROCESSED_DATA / printer.lower() / method.lower()

    # Creates dataframes for all enabled orientations
    orientations_data: dict[str, OrientationData] = {}
    for key in ['ML', 'CC', 'PD']:
        if orientations.get(key):
            dataframes = load_dataframes_from_files(path=data_path / key)
            orientations_data[key] = OrientationData(
                ultimate_strength=find_ultimate_strength(dataframes),
                youngs_modulus=find_youngs_modulus(dataframes)
            )
