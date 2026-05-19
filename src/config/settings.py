# src/config/settings.py
import pandas as pd


class Analysis:
    def __init__(self, median_graph_enabled, printer, method, orientations, disabled_tests):
        self.median_graph_enabled = median_graph_enabled
        self.printer = printer
        self.method = method
        self.orientations = orientations
        self.disabled_tests = disabled_tests


class OrientationData:
    def __init__(self, *, total_energy, ultimate_strength, youngs_modulus):
        self.total_energy:float = total_energy
        self.ultimate_strength: float = ultimate_strength
        self.youngs_modulus: float = youngs_modulus

    def __str__(self) -> str:
        return (
            f"  Total Energy        : {self.total_energy:.3f} MPa\n"
            f"  Ultimate Strength   : {self.ultimate_strength:.3f} MPa\n"
            f"  Young's Modulus     : {self.youngs_modulus:.3f}"
        )


FILL_COLOR = '#C2C2C2'
# COLORS = {
#     'medial-lateral': '#929292',
#     'cranial-caudal': '#616161',
#     'proximal-distal': '#313131'
# }

COLORS = {
    'medial-lateral': 'darkgreen',
    'cranial-caudal': 'darkred',
    'proximal-distal': 'mediumblue'
}

QUICK_GRAPH = False

SKIPPED_TESTS = []

DEFAULT_SKIPPED_TESTS = [
    'BMF_BEAM_THREE8',
    'BMF_BEAM_THREE9',
    'BMF_BEAM_THREE11',
    'BMF_BEAM_THREE12',

    'BMF_BEAM_ONE3',
]
