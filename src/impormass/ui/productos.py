# src/impormass/ui/productos.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import producto_service as svc
from ..utils.ui_helpers import auto_resize_treeview

BG = "#f8f8f8"

# ---------- CONSULTA ----------
def vista_consulta(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    frame.rowconfigure(2, weight=1)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="CONSULTA DE PRODUCTOS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    barra = tk.Frame(frame, bg=BG)
    barra.grid(row=1, column=0, sticky="ew", padx=12)
    barra.columnconfigure(1, weight=1)

    tk.Label(barra, text="Buscar:", bg=BG, font=("Segoe UI", 11))\
        .grid(row=0, column=0, padx=(0,8), pady=6, sticky="w")
    entrada = tk.Entry(barra, font=("Segoe UI", 12))
    entrada.grid(row=0, column=1, sticky="ew", pady=6)

    tabla_wrap = tk.Frame(frame)
    tabla_wrap.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)
    tabla_wrap.rowconfigure(0, weight=1); tabla_wrap.columnconfigure(0, weight=1)

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

    tk.Button(frame, text="⬅ Volver", command=volver_funcion)\
        .grid(row=3, column=0, pady=(4, 12))

# ---------- REGISTRO / CRUD ----------
def vista_registro(frame, volver_funcion):
    for w in frame.winfo_children(): w.destroy()

    frame.rowconfigure(3, weight=1)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="REGISTRO DE PRODUCTOS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    # Formulario (2 columnas elásticas)
    form = tk.Frame(frame, bg=BG); form.grid(row=1, column=0, sticky="ew", padx=12)
    for c in (0,1): form.columnconfigure(c, weight=1)

    def _row(r, text, widget):
        tk.Label(form, text=text, bg=BG, font=("Segoe UI", 11))\
            .grid(row=2*r, column=0, sticky="w", pady=(4,0), padx=(0,6))
        widget.grid(row=2*r+1, column=0, columnspan=2, sticky="ew", padx=(0,6), pady=(0,4))

    e_nombre = tk.Entry(form, font=("Segoe UI", 12))
    e_codigo = tk.Entry(form, font=("Segoe UI", 12))
    e_precio = tk.Entry(form, font=("Segoe UI", 12))
    e_cant   = tk.Entry(form, font=("Segoe UI", 12))
    e_desc   = tk.Text (form, font=("Segoe UI", 12), height=4)

    _row(0, "Nombre del producto", e_nombre)
    _row(1, "Código (opcional)", e_codigo)
    _row(2, "Precio (S/.)", e_precio)
    _row(3, "Cantidad", e_cant)
    _row(4, "Descripción", e_desc)

    # Barra búsqueda
    barra = tk.Frame(frame, bg=BG); barra.grid(row=2, column=0, sticky="ew", padx=12, pady=(6,0))
    barra.columnconfigure(1, weight=1)
    tk.Label(barra, text="🔍 Buscar:", bg=BG).grid(row=0, column=0, padx=(0,6))
    e_buscar = tk.Entry(barra, font=("Segoe UI", 12))
    e_buscar.grid(row=0, column=1, sticky="ew")

    # Tabla
    wrap = tk.Frame(frame); wrap.grid(row=3, column=0, sticky="nsew", padx=12, pady=10)
    wrap.rowconfigure(0, weight=1); wrap.columnconfigure(0, weight=1)

    cols = ("Código", "Nombre", "Precio", "Cantidad", "Descripción")
    tree = ttk.Treeview(wrap, columns=cols, show="headings")
    for c in cols: tree.heading(c, text=c)
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

    # Acciones
    def _clean():
        for e in (e_codigo, e_nombre, e_precio, e_cant): e.delete(0, tk.END)
        e_desc.delete("1.0", tk.END)

    def _sel_to_inputs():
        sel = tree.focus()
        if not sel: return None
        v = tree.item(sel, "values")
        _clean()
        e_codigo.insert(0, v[0]); e_nombre.insert(0, v[1])
        e_precio.insert(0, v[2]); e_cant.insert(0, v[3])
        e_desc.insert("1.0", v[4])
        return v[0]

    def guardar():
        nombre = e_nombre.get().strip()
        codigo = e_codigo.get().strip()
        precio = e_precio.get().strip()
        cant   = e_cant.get().strip()
        desc   = e_desc.get("1.0", tk.END).strip()
        if not (nombre and precio and cant):
            messagebox.showwarning("Campos", "Nombre, precio y cantidad son obligatorios."); return
        try:
            precio = float(precio); cant = int(cant)
        except ValueError:
            messagebox.showwarning("Valor", "Precio y cantidad deben ser números."); return
        if codigo and svc.existe_codigo(codigo):
            messagebox.showerror("Código duplicado", "Ya existe un producto con ese código."); return
        svc.crear(nombre, codigo or None, precio, cant, desc)
        _clean(); cargar(); messagebox.showinfo("OK", "Producto guardado.")

    def eliminar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Elige un producto."); return
        codigo = tree.item(sel, "values")[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar {codigo}?"):
            svc.eliminar(codigo); cargar(); messagebox.showinfo("OK", "Eliminado.")

    def actualizar():
        codigo = _sel_to_inputs()
        if not codigo:
            messagebox.showwarning("Selección", "Elige un producto para editar."); return
        try:
            precio = float(e_precio.get()); cant = int(e_cant.get())
        except ValueError:
            messagebox.showwarning("Valor", "Precio y cantidad deben ser números."); return
        svc.actualizar(codigo=codigo,
                       nombre=e_nombre.get().strip(),
                       precio=precio,
                       cantidad=cant,
                       descripcion=e_desc.get("1.0", tk.END).strip())
        _clean(); cargar(); messagebox.showinfo("OK", "Actualizado.")

    # Botoneras
    acc = tk.Frame(frame, bg=BG); acc.grid(row=4, column=0, pady=(4, 8))
    for i, (txt, cmd) in enumerate([
        ("✏ Cargar para editar", _sel_to_inputs),
        ("✅ Actualizar", actualizar),
        ("🛑 Cancelar edición", _clean),
        ("❌ Eliminar", eliminar),
        ("💾 Guardar Producto", guardar),
    ]):
        tk.Button(acc, text=txt, command=cmd).grid(row=0, column=i, padx=5)

    tk.Button(frame, text="⬅ Volver", command=volver_funcion)\
        .grid(row=5, column=0, pady=(4, 12))
