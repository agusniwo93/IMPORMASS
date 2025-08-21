# src/impormass/utils/ui_helpers.py
import tkinter as tk
from tkinter import ttk

def make_window_responsive(root: tk.Misc):
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

def make_frame_responsive(frame: tk.Frame, rows=(0,), cols=(0,)):
    for r in rows: frame.rowconfigure(r, weight=1)
    for c in cols: frame.columnconfigure(c, weight=1)

def auto_resize_treeview(tree: ttk.Treeview, fractions=None, min_px=80):
    cols = tree["columns"]
    if not cols:
        return
    if fractions is None:
        fractions = [1 / len(cols)] * len(cols)
    fractions = fractions + [0] * (len(cols) - len(fractions))

    def _resize(_e=None):
        total = max(tree.winfo_width() - 20, min_px * len(cols))
        for col, frac in zip(cols, fractions):
            tree.column(col, width=max(int(total * frac), min_px))
    tree.bind("<Configure>", _resize)
    tree.after(200, _resize)

def load_optiondb_defaults(root: tk.Tk):
    # Usa llaves para familias con espacio
    root.option_add("*Font", "{Segoe UI} 11")
    root.option_add("*TButton*Font", "{Segoe UI} 11")
    root.option_add("*TLabel*Font", "{Segoe UI} 11")

    # Paddings por defecto para ttk
    root.option_add("*TButton.Padding", 6)
    root.option_add("*TLabel.Padding", 2)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass