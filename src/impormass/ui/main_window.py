# src/impormass/ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ..config import ASSETS
from .productos import vista_registro, vista_consulta
from .facturas import ventana_facturas_registro
from .clientes import vista_clientes
from .ver_facturas import vista_ver_facturas
from .configuracion import vista_configuracion

BG = "#f8f8f8"
BTN_BG = "#007acc"
BTN_FG = "white"
BTN_ACTIVE = "#005f99"

# Permisos por rol:
#  admin      -> todo + gestión de usuarios
#  vendedor   -> facturas, ver facturas, clientes
#  almacenero -> productos (registro y consulta)
PERMISOS = {
    "admin":      {"crear_factura", "ver_facturas", "clientes", "productos", "configuracion", "usuarios"},
    "vendedor":   {"crear_factura", "ver_facturas", "clientes"},
    "almacenero": {"productos"},
}


class MainApp(tk.Tk):
    def __init__(self, usuario="", rol="vendedor"):
        super().__init__()
        self.usuario = usuario
        self.rol = rol or "vendedor"
        self.permisos = PERMISOS.get(self.rol, PERMISOS["vendedor"])

        self.title("Facturador Electrónico SUNAT - IMPORMASS")
        self.geometry("1100x750")
        self.minsize(900, 600)
        self.configure(bg=BG)

        # --- Barra superior ---
        self._barra_top = tk.Frame(self, bg="#005f99", height=40)
        self._barra_top.grid(row=0, column=0, sticky="ew")
        self._barra_top.grid_propagate(False)

        tk.Label(self._barra_top, text="IMPORMASS - Sistema de Ventas y Almacén",
                 font=("Segoe UI", 10, "bold"), bg="#005f99", fg="white")\
            .pack(side="left", padx=12, pady=6)

        # Info del usuario y rol
        rol_display = self.rol.upper()
        tk.Label(self._barra_top,
                 text=f"Usuario: {self.usuario}  |  Rol: {rol_display}",
                 font=("Segoe UI", 9), bg="#005f99", fg="#cce5ff")\
            .pack(side="right", padx=(0, 8), pady=6)

        tk.Button(self._barra_top, text="Cerrar Sesión", font=("Segoe UI", 9),
                  bg="#cc3333", fg="white", relief="flat", activebackground="#aa2222",
                  command=self._cerrar_sesion)\
            .pack(side="right", padx=(0, 12), pady=4)

        self.rowconfigure(0, weight=0)   # barra top fija
        self.rowconfigure(1, weight=1)   # contenido crece
        self.columnconfigure(0, weight=1)

        self.frame_contenido = tk.Frame(self, bg=BG)
        self.frame_contenido.grid(row=1, column=0, sticky="nsew")
        self.frame_contenido.rowconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(0, weight=1)

        self._logo_orig = None
        self._logo_label = None

        self.menu_principal()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _clear(self):
        """Limpia el contenedor y resetea grid weights."""
        try:
            self.frame_contenido.unbind("<Configure>")
        except Exception:
            pass
        for w in self.frame_contenido.winfo_children():
            w.destroy()
        self._logo_label = None
        self._logo_orig = None
        # Reset grid weights
        for i in range(10):
            self.frame_contenido.rowconfigure(i, weight=0)
            self.frame_contenido.columnconfigure(i, weight=0)
        self.frame_contenido.rowconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(0, weight=1)

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar sesión?"):
            self.destroy()
            from .login import run_login
            run_login()

    def _resize_logo(self, _e=None):
        lbl = self._logo_label
        if not (self._logo_orig and lbl):
            return
        try:
            if not lbl.winfo_exists():
                return
        except Exception:
            return

        ancho_max = max(min(700, self.frame_contenido.winfo_width() - 80), 50)
        alto_max  = max(min(300, self.frame_contenido.winfo_height() - 300), 50)
        if ancho_max <= 0 or alto_max <= 0:
            return

        a0, b0 = self._logo_orig.size
        prop = min(ancho_max / a0, alto_max / b0, 1.0)
        img = self._logo_orig.resize((int(a0 * prop), int(b0 * prop)), Image.LANCZOS)
        pimg = ImageTk.PhotoImage(img)
        lbl.configure(image=pimg)
        lbl.image = pimg

    # ------------------------------------------------------------------
    # Menú Principal  (filtrado por rol)
    # ------------------------------------------------------------------
    def menu_principal(self):
        self._clear()

        cont = tk.Frame(self.frame_contenido, bg=BG)
        cont.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        cont.rowconfigure(0, weight=0)
        cont.rowconfigure(1, weight=1)
        cont.columnconfigure(0, weight=1)

        # Logo
        logo_wrap = tk.Frame(cont, bg=BG)
        logo_wrap.grid(row=0, column=0, sticky="n", pady=(10, 20))

        try:
            self._logo_orig = Image.open(ASSETS / "logo_impormass.png")
            self._logo_label = tk.Label(logo_wrap, bg=BG)
            self._logo_label.grid(row=0, column=0)
            self.frame_contenido.bind("<Configure>", self._resize_logo)
            self.after(150, self._resize_logo)
        except Exception:
            tk.Label(logo_wrap, text="IMPORMASS",
                     font=("Arial", 30, "bold"), bg=BG, fg="#007acc")\
                .grid(row=0, column=0)

        # Botones filtrados por permisos del rol
        btns = tk.Frame(cont, bg=BG)
        btns.grid(row=1, column=0, sticky="n", pady=(0, 8))
        btns.columnconfigure(0, weight=1)

        todas_opciones = [
            ("Crear Factura",    self._ir_crear_factura,    "crear_factura"),
            ("Ver Facturas",     self._ir_ver_facturas,     "ver_facturas"),
            ("Clientes",         self._ir_clientes,         "clientes"),
            ("Productos",        self.menu_productos,       "productos"),
            ("Gestión Usuarios", self._ir_usuarios,         "usuarios"),
            ("Configuracion",    self._ir_configuracion,     "configuracion"),
        ]

        row_idx = 0
        for txt, cmd, permiso in todas_opciones:
            if permiso in self.permisos:
                tk.Button(btns, text=txt, font=("Segoe UI", 14), width=25,
                          height=2, bg=BTN_BG, fg=BTN_FG,
                          activebackground=BTN_ACTIVE, relief="flat",
                          command=cmd)\
                    .grid(row=row_idx, column=0, sticky="ew", padx=6, pady=6)
                row_idx += 1

    # ------------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------------
    def _ir_crear_factura(self):
        self._clear()
        ventana_facturas_registro(self.frame_contenido, self.menu_principal)

    def _ir_ver_facturas(self):
        self._clear()
        vista_ver_facturas(self.frame_contenido, self.menu_principal)

    def _ir_clientes(self):
        self._clear()
        vista_clientes(self.frame_contenido, self.menu_principal)

    def _ir_configuracion(self):
        self._clear()
        vista_configuracion(self.frame_contenido, self.menu_principal)

    # --- Sub-menú Productos ---
    def menu_productos(self):
        self._clear()

        cont = tk.Frame(self.frame_contenido, bg=BG)
        cont.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        cont.rowconfigure(0, weight=0)
        cont.rowconfigure(1, weight=1)
        cont.columnconfigure(0, weight=1)

        tk.Label(cont, text="GESTIÓN DE PRODUCTOS",
                 font=("Segoe UI", 18, "bold"), bg=BG)\
            .grid(row=0, column=0, pady=(8, 16), sticky="n")

        btns = tk.Frame(cont, bg=BG)
        btns.grid(row=1, column=0, sticky="n", pady=(0, 8))
        btns.columnconfigure(0, weight=1)

        opciones_prod = [
            ("Registrar Producto", lambda: self._ir_vista_prod(vista_registro)),
            ("Consultar Productos", lambda: self._ir_vista_prod(vista_consulta)),
        ]
        for i, (txt, cmd) in enumerate(opciones_prod):
            tk.Button(btns, text=txt, font=("Segoe UI", 13), width=25,
                      height=2, bg=BTN_BG, fg=BTN_FG,
                      activebackground=BTN_ACTIVE, relief="flat",
                      command=cmd)\
                .grid(row=i, column=0, sticky="ew", padx=6, pady=6)

        tk.Button(btns, text="Volver al Menu Principal",
                  font=("Segoe UI", 13), width=25, height=2,
                  command=self.menu_principal)\
            .grid(row=2, column=0, sticky="ew", padx=6, pady=6)

    def _ir_vista_prod(self, vista_fn):
        self._clear()
        vista_fn(self.frame_contenido, self.menu_productos)

    # ------------------------------------------------------------------
    # Gestión de Usuarios (solo admin)
    # ------------------------------------------------------------------
    def _ir_usuarios(self):
        from ..services import auth_service as auth_svc
        from ..utils.ui_helpers import auto_resize_treeview

        self._clear()
        f = self.frame_contenido
        for i in range(6):
            f.rowconfigure(i, weight=0)
        f.rowconfigure(3, weight=1)
        f.columnconfigure(0, weight=1)

        tk.Label(f, text="GESTIÓN DE USUARIOS",
                 font=("Segoe UI", 20, "bold"), bg=BG)\
            .grid(row=0, column=0, pady=(14, 8), sticky="n")

        # Formulario de registro rápido
        form = tk.Frame(f, bg=BG)
        form.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        for c in range(4):
            form.columnconfigure(c, weight=1 if c < 3 else 0)

        tk.Label(form, text="Usuario:", bg=BG, font=("Segoe UI", 10))\
            .grid(row=0, column=0, sticky="e", padx=4)
        e_user = tk.Entry(form, font=("Segoe UI", 11), width=18)
        e_user.grid(row=0, column=1, sticky="w", padx=4)

        tk.Label(form, text="Contraseña:", bg=BG, font=("Segoe UI", 10))\
            .grid(row=1, column=0, sticky="e", padx=4)
        e_pass = tk.Entry(form, font=("Segoe UI", 11), show="*", width=18)
        e_pass.grid(row=1, column=1, sticky="w", padx=4)

        tk.Label(form, text="Rol:", bg=BG, font=("Segoe UI", 10))\
            .grid(row=0, column=2, sticky="e", padx=4)
        cb_rol = ttk.Combobox(form, values=["admin", "vendedor", "almacenero"],
                               state="readonly", width=14, font=("Segoe UI", 11))
        cb_rol.set("vendedor")
        cb_rol.grid(row=0, column=3, sticky="w", padx=4)

        # Tabla de usuarios
        wrap = tk.Frame(f)
        wrap.grid(row=3, column=0, sticky="nsew", padx=12, pady=6)
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        cols = ("ID", "Usuario", "Rol")
        tree = ttk.Treeview(wrap, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
        tree.column("ID", width=50)
        tree.grid(row=0, column=0, sticky="nsew")
        auto_resize_treeview(tree, fractions=[0.10, 0.50, 0.40])

        sy = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscroll=sy.set)
        sy.grid(row=0, column=1, sticky="ns")

        def cargar():
            tree.delete(*tree.get_children())
            for fila in auth_svc.listar_usuarios():
                tree.insert("", tk.END, values=fila)

        cargar()

        # Botones
        acc = tk.Frame(f, bg=BG)
        acc.grid(row=4, column=0, pady=(4, 4))

        def crear_usuario():
            u = e_user.get().strip()
            p = e_pass.get().strip()
            r = cb_rol.get()
            if not u or not p:
                messagebox.showwarning("Campos", "Usuario y contraseña son obligatorios.")
                return
            if len(p) < 4:
                messagebox.showwarning("Contraseña", "Mínimo 4 caracteres.")
                return
            if auth_svc.registrar(u, p, r):
                messagebox.showinfo("OK", f"Usuario '{u}' creado con rol '{r}'.")
                e_user.delete(0, tk.END)
                e_pass.delete(0, tk.END)
                cargar()
            else:
                messagebox.showerror("Error", "El usuario ya existe.")

        def cambiar_rol():
            sel = tree.focus()
            if not sel:
                messagebox.showwarning("Selección", "Selecciona un usuario.")
                return
            vals = tree.item(sel, "values")
            uid = int(vals[0])
            nuevo = cb_rol.get()
            auth_svc.cambiar_rol(uid, nuevo)
            messagebox.showinfo("OK", f"Rol de '{vals[1]}' cambiado a '{nuevo}'.")
            cargar()

        def eliminar_usr():
            sel = tree.focus()
            if not sel:
                messagebox.showwarning("Selección", "Selecciona un usuario.")
                return
            vals = tree.item(sel, "values")
            uid = int(vals[0])
            nombre = vals[1]
            if nombre == self.usuario:
                messagebox.showwarning("No permitido", "No puedes eliminar tu propio usuario.")
                return
            if messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{nombre}'?"):
                auth_svc.eliminar_usuario(uid)
                cargar()

        tk.Button(acc, text="Crear Usuario", font=("Segoe UI", 9),
                  command=crear_usuario).grid(row=0, column=0, padx=4)
        tk.Button(acc, text="Cambiar Rol", font=("Segoe UI", 9),
                  command=cambiar_rol).grid(row=0, column=1, padx=4)
        tk.Button(acc, text="Eliminar", font=("Segoe UI", 9),
                  bg="#cc3333", fg="white",
                  command=eliminar_usr).grid(row=0, column=2, padx=4)

        tk.Button(f, text="Volver al Menu Principal", font=("Segoe UI", 11, "bold"),
                  command=self.menu_principal, bg="#007acc", fg="white",
                  activebackground="#005f99", relief="flat", padx=16, pady=4)\
            .grid(row=5, column=0, pady=(4, 12))
