# src/pipeline/run_pipeline.py
from src.config.settings import *
from src.pipeline.preprocessing import *
import src.config.paths as paths
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import openpyxl


def generate_graph(analysis: Analysis):
    median_graph_enabled, printer, method, orientations, disabled_tests = (
        analysis.vget(analysis.median_graph_enabled), analysis.vget(analysis.printer), analysis.vget(analysis.method),
        analysis.orientations, analysis.disabled_tests)

    # Handle both tkinter (list of (tree, checked) tuples) and ipywidgets (list of paths)
    if disabled_tests and isinstance(disabled_tests[0], tuple):
        # tkinter format
        unselected = [
            tree.item(iid, "text").split(" ", 1)[1]
            for tree, checked in disabled_tests
            for iid, var in checked.items()
            if not var.get()
        ]
    else:
        # ipywidgets format — already a list of unchecked file paths
        unselected = disabled_tests

    for file in unselected:
        SKIPPED_TESTS.append(file)

    ax = plt.subplot()
    handles = []

    # The location of the files used for the graph based on user config (analysis)
    data_path = paths.PROCESSED_DATA / printer.lower() / method.lower()

    # Creates dataframes for all enabled orientations
    orientations_data: dict[str, OrientationData] = {}
    for key in ['medial-lateral', 'cranial-caudal', 'proximal-distal']:
        if analysis.vget(orientations.get(key)):
            print("scanning " + key)
            current_orientation = load_dataframes_from_files(path=data_path / key)

            total_energy = find_total_energy(current_orientation)
            ultimate_strength = find_ultimate_strength(current_orientation)
            youngs_modulus = find_youngs_modulus(current_orientation)  # [E, all_window_bounds]

            orientations_data[key] = OrientationData(
                total_energy=total_energy,
                ultimate_strength=ultimate_strength,
                youngs_modulus=youngs_modulus[0],
            )
            if median_graph_enabled:
                median_dataframe = calculate_median_graph(current_orientation)
                plt.plot(median_dataframe.loc[:, 'Strain'] * 1000000,
                         median_dataframe.loc[:, 'Stress'],
                         c=COLORS[key])
                print(np.median(youngs_modulus[1][0]))
                print(np.median(youngs_modulus[1][1]))
                plt.axvspan(np.median(youngs_modulus[1][0]) * 1e6, np.median(youngs_modulus[1][1]) * 1e6,
                            color=np.random.rand(3), alpha=0.2, label="Linear Region")
            else:
                for test in current_orientation:
                    plt.plot(test.loc[:, 'Strain'] * 1000000,
                             test.loc[:, 'Stress'],
                             c=COLORS[key])
                for i in range(len(youngs_modulus[1][0])):
                    plt.axvspan(youngs_modulus[1][0][i] * 1e6, youngs_modulus[1][1][i] * 1e6,
                                color=np.random.rand(3), alpha=0.2)
            printer_formatted = printer.upper() if printer.lower() == 'bmf' else printer.capitalize()
            median_text = "Median" if median_graph_enabled else ""
            handles.append(patches.Patch(color=COLORS[key],
                                         label=f"{printer_formatted} {key.title()} {method.title()} {median_text}"))

    for key, value in orientations_data.items():
        print(key.replace('-', ' ').title())
        print(value)
        print()

    plt.xlabel('Microstrain (\u03BC\u03B5)')
    plt.ylabel('Stress (MPa)')
    ax.legend(handles=handles)
    plt.title = 'Brand new gui for trabecular bone analysis'
    plt.xlim(0, 400000)
    plt.ylim(0, 17.5)
    plt.show()
