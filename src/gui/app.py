# src/gui/app.py
import tkinter as tk
from tkinter import ttk
import src.config.generation_settings as generation_settings
import sv_ttk
import src.pipeline.run_pipeline as run_pipeline


def main():
    root = tk.Tk()
    root.title('3DP Bone Analysis')

    m = ttk.Frame(root, padding=20)
    m.grid(row=0, column=0, sticky="ew")

    printer_label = ttk.Label(m, text="Select a printer:")
    printer_label.grid(row=0, column=0, pady=10, padx=0, sticky="w")
    printer_box = ttk.Combobox(m, values=["BMF", "Formlabs"], state='readonly')
    printer_box.grid(row=0, column=1, pady=10, padx=20, sticky="ew")
    printer_box.set("BMF")

    method_label = ttk.Label(m, text="Select a test method:")
    method_label.grid(row=1, column=0, pady=10, sticky="w")
    method_box = ttk.Combobox(m, values=["Tension", "Compression"], state='readonly')
    method_box.grid(row=1, column=1, pady=10, padx=20, sticky="ew")
    method_box.set("Tension")

    checkboxes = ttk.Frame(m)
    checkboxes.grid(row=2, column=1, sticky="w", padx=20, pady=(5, 10))
    orientations_label = ttk.Label(m, text="Select orientations:")
    orientations_label.grid(row=2, column=0, pady=0, padx=15, sticky="w")

    medial_lateral_enabled = tk.BooleanVar(value=True)
    cranial_caudal_enabled = tk.BooleanVar(value=True)
    proximal_distal_enabled = tk.BooleanVar(value=True)

    medial_lateral_checkbox = ttk.Checkbutton(checkboxes, text="Medial-Lateral", variable=medial_lateral_enabled)
    medial_lateral_checkbox.grid(row=0, column=0, padx=5, sticky="w")
    cranial_caudal_checkbox = ttk.Checkbutton(checkboxes, text="Cranial-Caudal", variable=cranial_caudal_enabled)
    cranial_caudal_checkbox.grid(row=0, column=1, padx=5, sticky="w")
    proximal_distal_checkbox = ttk.Checkbutton(checkboxes, text="Proximal-Distal", variable=proximal_distal_enabled)
    proximal_distal_checkbox.grid(row=0, column=2, padx=5, sticky="w")

    orientations = {
        'ML': medial_lateral_enabled,
        'CC': cranial_caudal_enabled,
        'PD': proximal_distal_enabled
    }

    current_analysis = generation_settings.Analysis(printer_box, method_box, orientations)
    start_button = ttk.Button(m, text="Generate Graph", command=lambda: run_pipeline.generate_graph(current_analysis))
    start_button.grid(row=1, column=2)

    progress_bar_frame = ttk.Frame(m)
    progress_bar_frame.grid(row=2, column=2, sticky="w", padx=20, pady=(5, 10))
    progress = ttk.Progressbar(progress_bar_frame, mode="indeterminate", maximum=100)
    progress.grid(row=0, column=0, sticky="we")
    # progress.grid_remove()

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=1)
    m.columnconfigure(0, weight=0)
    m.columnconfigure(1, weight=1)
    m.columnconfigure(2, weight=0)
    m.rowconfigure(0, weight=1)

    root.minsize(800, 1)

    printer_box.bind("<<ComboboxSelected>>", lambda e: e.widget.after_idle(e.widget.selection_clear))
    method_box.bind("<<ComboboxSelected>>", lambda e: e.widget.after_idle(e.widget.selection_clear))

    sv_ttk.use_dark_theme()
    m.mainloop()
