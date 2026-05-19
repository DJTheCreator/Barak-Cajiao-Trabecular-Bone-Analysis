# src/gui/app.py
import os
import tkinter as tk
from tkinter import ttk
import src.config.settings as generation_settings
import src.config.paths as paths
import sv_ttk
import src.pipeline.run_pipeline as run_pipeline
from src import config


def build_file_tree(parent, root_path, label_text, column):
    frame = ttk.LabelFrame(parent, text=label_text, padding=10)
    frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")

    tree = ttk.Treeview(frame, show="tree", selectmode="none")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    checked = {}  # item_id -> BooleanVar

    def insert_node(parent_id, path):
        name = os.path.basename(path)

        if not os.path.isdir(path) and name in generation_settings.DEFAULT_SKIPPED_TESTS:
            return None

        var = tk.BooleanVar(value=True)
        display = f"☑ {name}"
        item_id = tree.insert(parent_id, "end", text=display, open=True)
        checked[item_id] = var

        if os.path.isdir(path):
            for child in sorted(os.listdir(path)):
                insert_node(item_id, os.path.join(path, child))

        return item_id

    def toggle(item_id, value):
        checked[item_id].set(value)
        symbol = "☑" if value else "☐"
        name = tree.item(item_id, "text").split(" ", 1)[1]
        tree.item(item_id, text=f"{symbol} {name}")
        for child in tree.get_children(item_id):
            toggle(child, value)

    def on_click(event):
        item_id = tree.identify_row(event.y)
        if item_id:
            toggle(item_id, not checked[item_id].get())

    tree.bind("<Button-1>", on_click)

    if os.path.exists(root_path):
        insert_node("", root_path)
    else:
        tree.insert("", "end", text=f"(path not found: {root_path})")

    return tree, checked


def main():
    root = tk.Tk()
    root.title('3DP Bone Analysis')

    tabControl = ttk.Notebook(root)
    tabControl.grid(row=0, column=0, sticky="nsew")

    tab1 = ttk.Frame(tabControl, padding=20)
    tabControl.add(tab1, text="Analysis")
    # tab1.grid(row=0, column=0, sticky="ew")

    tab2 = ttk.Frame(tabControl, padding=20)
    tabControl.add(tab2, text="Files")

    printer_label = ttk.Label(tab1, text="Select a printer:")
    printer_label.grid(row=0, column=0, pady=10, padx=0, sticky="w")
    printer_box = ttk.Combobox(tab1, values=["BMF", "Formlabs"], state='readonly')
    printer_box.grid(row=0, column=1, pady=10, padx=20, sticky="ew")
    printer_box.set("BMF")

    method_label = ttk.Label(tab1, text="Select a test method:")
    method_label.grid(row=1, column=0, pady=10, sticky="w")
    method_box = ttk.Combobox(tab1, values=["Tension", "Compression"], state='readonly')
    method_box.grid(row=1, column=1, pady=10, padx=20, sticky="ew")
    method_box.set("Tension")

    checkboxes = ttk.Frame(tab1)
    checkboxes.grid(row=2, column=1, sticky="w", padx=20, pady=(5, 10))
    orientations_label = ttk.Label(tab1, text="Select orientations:")
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
        'medial-lateral': medial_lateral_enabled,
        'cranial-caudal': cranial_caudal_enabled,
        'proximal-distal': proximal_distal_enabled
    }

    median_graph_enabled = tk.BooleanVar(value=True)
    median_checkbox = ttk.Checkbutton(tab1, text="Median Graph", variable=median_graph_enabled)
    median_checkbox.grid(row=0, column=2, sticky="w")

    # ------------ Tab 2 ----------------

    tree_CC, checked_CC = build_file_tree(tab2, paths.PROCESSED_DATA / 'bmf' / 'tension' / 'Cranial-Caudal',
                                          "Cranial-Caudal", column=0)
    tree_ML, checked_ML = build_file_tree(tab2, paths.PROCESSED_DATA / 'bmf' / 'tension' / 'Medial-Lateral',
                                          "Medial-Lateral", column=1)
    tree_PD, checked_PD = build_file_tree(tab2, paths.PROCESSED_DATA / 'bmf' / 'tension' / 'Proximal-Distal',
                                          "Proximal-Distal", column=2)

    all_trees = [(tree_CC, checked_CC), (tree_ML, checked_ML), (tree_PD, checked_PD)]

    unselected = [
        tree.item(iid, "text").split(" ", 1)[1]
        for tree, checked in all_trees
        for iid, var in checked.items()
        if not var.get()
    ]

    # ---------- Interaction ------------

    current_analysis = generation_settings.Analysis(median_graph_enabled, printer_box, method_box, orientations, unselected)
    start_button = ttk.Button(tab1, text="Generate Graph",
                              command=lambda: run_pipeline.generate_graph(current_analysis))
    start_button.grid(row=1, column=2)

    progress_bar_frame = ttk.Frame(tab1)
    progress_bar_frame.grid(row=2, column=2, sticky="w", padx=20, pady=(5, 10))
    progress = ttk.Progressbar(progress_bar_frame, mode="indeterminate", maximum=100)
    progress.grid(row=0, column=0, sticky="we")
    # progress.grid_remove()

    # ------------ Config ---------------

    style = ttk.Style()
    style.configure("TNotebook", tabposition="s")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # root.rowconfigure(1, weight=0)
    # root.rowconfigure(2, weight=1)
    tab1.columnconfigure(0, weight=0)
    tab1.columnconfigure(1, weight=1)
    tab1.columnconfigure(2, weight=0)
    tab1.rowconfigure(0, weight=0)
    tab1.rowconfigure(1, weight=0)
    tab1.rowconfigure(2, weight=0)

    root.minsize(800, 225)

    printer_box.bind("<<ComboboxSelected>>", lambda e: e.widget.after_idle(e.widget.selection_clear))
    method_box.bind("<<ComboboxSelected>>", lambda e: e.widget.after_idle(e.widget.selection_clear))

    sv_ttk.use_dark_theme()
    root.mainloop()
