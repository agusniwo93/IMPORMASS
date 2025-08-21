# src/impormass/ui/base.py
import tkinter as tk
from ..utils.ui_helpers import make_window_responsive, load_optiondb_defaults

class BaseWindow(tk.Tk):
    """Tk raíz con configuración responsive y defaults globales."""
    def __init__(self, title="IMPORMASS", size="1100x700", minsize=(900, 600), bg="#f8f8f8"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.minsize(*minsize)
        self.configure(bg=bg)

        # defaults visuales globales + grid root responsive
        load_optiondb_defaults(self)
        make_window_responsive(self)
