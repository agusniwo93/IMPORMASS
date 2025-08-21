# src/impormass/ui/main_window.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, Image  # asegúrate de importar Image
from ..config import ASSETS
from .productos import vista_registro, vista_consulta
from .facturas import ventana_facturas_registro


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Facturador Electrónico SUNAT")

        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg="#f8f8f8")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame_contenido = tk.Frame(self, bg="#f8f8f8")
        self.frame_contenido.grid(row=0, column=0, sticky="nsew")
        self.frame_contenido.rowconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(0, weight=1)

        self._logo_orig = None
        self._logo_label = None

        self.menu_principal()

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------
    def _clear(self):
        """Limpia el contenedor y elimina binds para evitar callbacks a widgets destruidos."""
        # 1) Desenlaza cualquier callback previo de <Configure>
        try:
            self.frame_contenido.unbind("<Configure>")
        except Exception:
            pass
        # 2) Destruye hijos
        for w in self.frame_contenido.winfo_children():
            w.destroy()
        # 3) Limpia referencias del logo
        self._logo_label = None
        self._logo_orig = None

    def _resize_logo(self, _e=None):
        """Redimensiona el logo si el label aún existe."""
        lbl = self._logo_label
        if not (self._logo_orig and lbl):
            return
        # El label puede haber sido destruido por un cambio de vista
        if not lbl.winfo_exists():
            return

        # Espacio disponible dentro del contenedor
        ancho_max = max(min(700, self.frame_contenido.winfo_width() - 80), 50)
        alto_max  = max(min(300, self.frame_contenido.winfo_height() - 300), 50)
        if ancho_max <= 0 or alto_max <= 0:
            return

        a0, b0 = self._logo_orig.size
        prop = min(ancho_max / a0, alto_max / b0, 1.0)
        # usa LANCZOS para mejor calidad
        img = self._logo_orig.resize((int(a0 * prop), int(b0 * prop)), Image.LANCZOS)
        pimg = ImageTk.PhotoImage(img)
        lbl.configure(image=pimg)
        lbl.image = pimg  # evita GC

    # ------------------------------------------------------
    # Vistas
    # ------------------------------------------------------
    def menu_principal(self):
        self._clear()

        cont = tk.Frame(self.frame_contenido, bg="#f8f8f8")
        cont.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        cont.rowconfigure(0, weight=0)  # logo
        cont.rowconfigure(1, weight=1)  # botones
        cont.columnconfigure(0, weight=1)

        # Logo (fila 0)
        logo_wrap = tk.Frame(cont, bg="#f8f8f8")
        logo_wrap.grid(row=0, column=0, sticky="n", pady=(10, 24))

        try:
            self._logo_orig = Image.open(ASSETS / "logo_impormass.png")
            self._logo_label = tk.Label(logo_wrap, bg="#f8f8f8")
            self._logo_label.grid(row=0, column=0)

            # Primero desenlaza por si venimos de otra vista, luego enlaza de nuevo
            self.frame_contenido.unbind("<Configure>")
            self.frame_contenido.bind("<Configure>", self._resize_logo)
            # Pintado inicial leve delay
            self.after(150, self._resize_logo)
        except Exception:
            tk.Label(
                logo_wrap,
                text="IMPORMASS",
                font=("Arial", 30, "bold"),
                bg="#f8f8f8",
                fg="#007acc",
            ).grid(row=0, column=0)

        # Columna de botones (fila 1)
        btns = tk.Frame(cont, bg="#f8f8f8")
        btns.grid(row=1, column=0, sticky="n", pady=(0, 8))
        btns.columnconfigure(0, weight=1)

        opciones = [
            ("📟 Crear Factura", lambda: (self._clear(),
                                         ventana_facturas_registro(self.frame_contenido, self.menu_principal))),
            ("📂 Ver Facturas", lambda: messagebox.showinfo("Ver Facturas", "Próximamente")),
            ("👥 Clientes",     lambda: messagebox.showinfo("Clientes", "Próximamente")),
            ("📦 Productos",    self.menu_productos),
            ("⚙ Configuración", lambda: messagebox.showinfo("Configuración", "Próximamente")),
        ]

        for i, (txt, cmd) in enumerate(opciones):
            tk.Button(
                btns, text=txt, font=("Segoe UI", 14),
                height=2, bg="#007acc", fg="white",
                activebackground="#005f99", relief="flat",
                command=cmd
            ).grid(row=i, column=0, sticky="ew", padx=6, pady=8)

    def menu_productos(self):
        self._clear()

        cont = tk.Frame(self.frame_contenido, bg="#f8f8f8")
        cont.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        cont.rowconfigure(0, weight=0)  # título
        cont.rowconfigure(1, weight=1)  # botones
        cont.columnconfigure(0, weight=1)

        tk.Label(
            cont,
            text="GESTIÓN DE PRODUCTOS",
            font=("Segoe UI", 18, "bold"),
            bg="#f8f8f8",
        ).grid(row=0, column=0, pady=(8, 16), sticky="n")

        btns = tk.Frame(cont, bg="#f8f8f8")
        btns.grid(row=1, column=0, sticky="n", pady=(0, 8))
        btns.columnconfigure(0, weight=1)

        def _btn(texto, cmd, row):
            tk.Button(
                btns,
                text=texto,
                font=("Segoe UI", 13),
                height=2,
                bg="#007acc",
                fg="white",
                activebackground="#005f99",
                relief="flat",
                command=cmd,
            ).grid(row=row, column=0, sticky="ew", padx=6, pady=8)

        _btn("📥 Registrar Producto",
             lambda: vista_registro(self.frame_contenido, self.menu_productos), 0)
        _btn("🔍 Consultar Productos",
             lambda: vista_consulta(self.frame_contenido, self.menu_productos), 1)
        tk.Button(
            btns,
            text="⬅ Volver al Menú Principal",
            font=("Segoe UI", 13),
            height=2,
            command=self.menu_principal,
        ).grid(row=2, column=0, sticky="ew", padx=6, pady=8)
