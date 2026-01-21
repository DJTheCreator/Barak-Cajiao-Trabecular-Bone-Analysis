# src/config/generation_settings.py
import pandas as pd


class Analysis:
    def __init__(self, printer, method, orientations):
        self.printer = printer
        self.method = method
        self.orientations = orientations


class OrientationData:
    def __init__(self, *, ultimate_strength, youngs_modulus):
        self.ultimate_strength: float = ultimate_strength
        self.youngs_modulus: float = youngs_modulus
