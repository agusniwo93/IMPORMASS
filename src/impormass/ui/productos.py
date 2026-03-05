# src/impormass/ui/productos.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import producto_service as svc
from ..utils.ui_helpers import auto_resize_treeview

BG = "#f8f8f8"


# ===================== CONSULTA =====================
def vista_consulta(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=0)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="CONSULTA DE PRODUCTOS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    barra = tk.Frame(frame, bg=BG)
    barra.grid(row=1, column=0, sticky="ew", padx=12)
    barra.columnconfigure(1, weight=1)

    tk.Label(barra, text="🔍 Buscar:", bg=BG, font=("Segoe UI", 11))\
        .grid(row=0, column=0, padx=(0, 8), pady=6, sticky="w")
    entrada = tk.Entry(barra, font=("Segoe UI", 12))
    entrada.grid(row=0, column=1, sticky="ew", pady=6)

    tabla_wrap = tk.Frame(frame)
    tabla_wrap.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)
    tabla_wrap.rowconfigure(0, weight=1)
    tabla_wrap.columnconfigure(0, weight=1)

    cols = ("Código", "Nombre", "Precio", "Cantidad", "Descripción")
    tree = ttk.Treeview(tabla_wrap, columns=cols, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")
    for c in cols:
        tree.heading(c, text=c)
    auto_resize_treeview(tree, fractions=[0.16, 0.28, 0.14, 0.14, 0.28])

    sy = ttk.Scrollbar(tabla_wrap, orient="vertical", command=tree.yview)
    sx = ttk.Scrollbar(tabla_wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=sy.set, xscroll=sx.set)
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")

    def cargar(f=""):
        tree.delete(*tree.get_children())
        for fila in svc.listar(f):
            tree.insert("", tk.END, values=fila)

    entrada.bind("<KeyRelease>", lambda e: cargar(entrada.get()))
    cargar()

    tk.Button(frame, text="Volver al Menu Productos", font=("Segoe UI", 11, "bold"),
              command=volver_funcion, bg="#007acc", fg="white",
              activebackground="#005f99", relief="flat", padx=16, pady=4)\
        .grid(row=3, column=0, pady=(4, 12))


# ===================== REGISTRO / CRUD =====================
def vista_registro(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=0)
    frame.rowconfigure(2, weight=0)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=0)
    frame.rowconfigure(5, weight=0)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="REGISTRO DE PRODUCTOS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    # --- Formulario (horizontal para aprovechar ancho) ---
    form = tk.Frame(frame, bg=BG)
    form.grid(row=1, column=0, sticky="ew", padx=12)
    for c in range(5):
        form.columnconfigure(c, weight=1)

    def _field(r, c, label_text, width=16):
        tk.Label(form, text=label_text, bg=BG, font=("Segoe UI", 10))\
            .grid(row=r * 2, column=c, sticky="w", padx=4, pady=(4, 0))
        e = tk.Entry(form, font=("Segoe UI", 11), width=width)
        e.grid(row=r * 2 + 1, column=c, sticky="ew", padx=4, pady=(0, 4))
        return e

    e_nombre = _field(0, 0, "Nombre del producto", 24)
    e_codigo = _field(0, 1, "Codigo (opcional)", 14)
    e_precio = _field(0, 2, "Precio (S/.)", 10)
    e_cant   = _field(0, 3, "Cantidad", 8)

    tk.Label(form, text="Descripcion", bg=BG, font=("Segoe UI", 10))\
        .grid(row=0, column=4, sticky="w", padx=4, pady=(4, 0))
    e_desc = tk.Text(form, font=("Segoe UI", 11), height=2, width=20)
    e_desc.grid(row=1, column=4, sticky="ew", padx=4, pady=(0, 4))

    # --- Barra búsqueda ---
    barra = tk.Frame(frame, bg=BG)
    barra.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 0))
    barra.columnconfigure(1, weight=1)
    tk.Label(barra, text="🔍 Buscar:", bg=BG).grid(row=0, column=0, padx=(0, 6))
    e_buscar = tk.Entry(barra, font=("Segoe UI", 12))
    e_buscar.grid(row=0, column=1, sticky="ew")

    # --- Tabla ---
    wrap = tk.Frame(frame)
    wrap.grid(row=3, column=0, sticky="nsew", padx=12, pady=10)
    wrap.rowconfigure(0, weight=1)
    wrap.columnconfigure(0, weight=1)

    cols = ("Código", "Nombre", "Precio", "Cantidad", "Descripción")
    tree = ttk.Treeview(wrap, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
    tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(tree, fractions=[0.16, 0.28, 0.14, 0.14, 0.28])

    sy = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
    sx = ttk.Scrollbar(wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=sy.set, xscroll=sx.set)
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")

    def cargar(f=""):
        tree.delete(*tree.get_children())
        for fila in svc.listar(f):
            tree.insert("", tk.END, values=fila)

    e_buscar.bind("<KeyRelease>", lambda e: cargar(e_buscar.get()))
    cargar()

    # --- Estado de edición ---
    editando = [False]

    def _clean():
        e_codigo.config(state="normal")
        for e in (e_codigo, e_nombre, e_precio, e_cant):
            e.delete(0, tk.END)
        e_desc.delete("1.0", tk.END)
        editando[0] = False
        lbl_estado.config(text="Modo: Nuevo producto", fg="#007acc")

    def _sel_to_inputs():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un producto de la tabla.")
            return None
        v = tree.item(sel, "values")
        _clean()
        e_codigo.insert(0, v[0])
        e_codigo.config(state="readonly")
        e_nombre.insert(0, v[1])
        e_precio.insert(0, v[2])
        e_cant.insert(0, v[3])
        e_desc.insert("1.0", v[4])
        editando[0] = True
        lbl_estado.config(text=f"Editando: {v[0]} - {v[1]}", fg="#cc6600")
        return v[0]

    def guardar():
        if editando[0]:
            messagebox.showinfo("Info", "Estás en modo edición. Usa 'Actualizar' o 'Cancelar' primero.")
            return
        nombre = e_nombre.get().strip()
        codigo = e_codigo.get().strip()
        precio = e_precio.get().strip()
        cant   = e_cant.get().strip()
        desc   = e_desc.get("1.0", tk.END).strip()
        if not (nombre and precio and cant):
            messagebox.showwarning("Campos", "Nombre, precio y cantidad son obligatorios.")
            return
        try:
            precio_f = float(precio)
            cant_i = int(cant)
        except ValueError:
            messagebox.showwarning("Valor", "Precio y cantidad deben ser números.")
            return
        if precio_f < 0 or cant_i < 0:
            messagebox.showwarning("Valor", "No pueden ser negativos.")
            return
        if codigo and svc.existe_codigo(codigo):
            messagebox.showerror("Código duplicado", "Ya existe un producto con ese código.")
            return
        svc.crear(nombre, codigo or None, precio_f, cant_i, desc)
        _clean()
        cargar(e_buscar.get())
        messagebox.showinfo("OK", "Producto guardado.")

    def actualizar():
        if not editando[0]:
            messagebox.showwarning("Selección", "Primero carga un producto para editar.")
            return
        codigo = e_codigo.get().strip()
        nombre = e_nombre.get().strip()
        precio_s = e_precio.get().strip()
        cant_s = e_cant.get().strip()
        desc = e_desc.get("1.0", tk.END).strip()
        if not (nombre and precio_s and cant_s):
            messagebox.showwarning("Campos", "Nombre, precio y cantidad son obligatorios.")
            return
        try:
            precio = float(precio_s)
            cant = int(cant_s)
        except ValueError:
            messagebox.showwarning("Valor", "Precio y cantidad deben ser números.")
            return
        svc.actualizar(codigo=codigo, nombre=nombre, precio=precio,
                       cantidad=cant, descripcion=desc)
        _clean()
        cargar(e_buscar.get())
        messagebox.showinfo("OK", "Producto actualizado.")

    def eliminar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Elige un producto de la tabla.")
            return
        vals = tree.item(sel, "values")
        codigo = vals[0]
        nombre = vals[1]
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}' ({codigo})?"):
            svc.eliminar(codigo)
            _clean()
            cargar(e_buscar.get())
            messagebox.showinfo("OK", "Producto eliminado.")

    # --- Botonera + indicador de estado ---
    acc = tk.Frame(frame, bg=BG)
    acc.grid(row=4, column=0, pady=(4, 4))

    lbl_estado = tk.Label(acc, text="Modo: Nuevo producto",
                          font=("Segoe UI", 9, "italic"), bg=BG, fg="#007acc")
    lbl_estado.grid(row=0, column=0, columnspan=5, pady=(0, 4))

    botones = [
        ("✏ Cargar para editar", _sel_to_inputs),
        ("✅ Actualizar", actualizar),
        ("🛑 Cancelar edición", _clean),
        ("❌ Eliminar", eliminar),
        ("💾 Guardar Nuevo", guardar),
    ]
    for i, (txt, cmd) in enumerate(botones):
        tk.Button(acc, text=txt, command=cmd, font=("Segoe UI", 9))\
            .grid(row=1, column=i, padx=4)

    tk.Button(frame, text="Volver al Menu Productos", font=("Segoe UI", 11, "bold"),
              command=volver_funcion, bg="#007acc", fg="white",
              activebackground="#005f99", relief="flat", padx=16, pady=4)\
        .grid(row=5, column=0, pady=(4, 12))
