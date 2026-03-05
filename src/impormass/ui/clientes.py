# src/impormass/ui/clientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import cliente_service as svc
from ..utils.ui_helpers import auto_resize_treeview

BG = "#f8f8f8"
TIPOS_DOC = ["RUC", "DNI", "CE"]


def vista_clientes(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    frame.rowconfigure(3, weight=1)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="GESTIÓN DE CLIENTES",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    # --- Formulario ---
    form = tk.Frame(frame, bg=BG)
    form.grid(row=1, column=0, sticky="ew", padx=12)
    for c in range(6):
        form.columnconfigure(c, weight=1)

    def _field(r, c, label_text, width=20):
        tk.Label(form, text=label_text, bg=BG, font=("Segoe UI", 10))\
            .grid(row=r*2, column=c, sticky="w", padx=4, pady=(4, 0))
        e = tk.Entry(form, font=("Segoe UI", 11), width=width)
        e.grid(row=r*2+1, column=c, sticky="ew", padx=4, pady=(0, 4))
        return e

    tk.Label(form, text="Tipo Doc.", bg=BG, font=("Segoe UI", 10))\
        .grid(row=0, column=0, sticky="w", padx=4, pady=(4, 0))
    cb_tipo = ttk.Combobox(form, values=TIPOS_DOC, state="readonly", width=8,
                           font=("Segoe UI", 11))
    cb_tipo.set("RUC")
    cb_tipo.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 4))

    e_numdoc = _field(0, 1, "Nro. Documento")
    e_razon = _field(0, 2, "Razón Social", 30)
    e_dir = _field(0, 3, "Dirección", 30)
    e_tel = _field(0, 4, "Teléfono", 14)
    e_email = _field(0, 5, "Email", 22)

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

    cols = ("ID", "Tipo Doc.", "Nro. Documento", "Razón Social",
            "Dirección", "Teléfono", "Email")
    tree = ttk.Treeview(wrap, columns=cols, show="headings")
    for c_name in cols:
        tree.heading(c_name, text=c_name)
    tree.column("ID", width=40)
    tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(tree, fractions=[0.05, 0.08, 0.12, 0.25, 0.22, 0.12, 0.16])

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

    # --- Acciones ---
    def _clean():
        cb_tipo.set("RUC")
        for e in (e_numdoc, e_razon, e_dir, e_tel, e_email):
            e.delete(0, tk.END)

    _editing_id = [None]

    def _sel_to_inputs():
        sel = tree.focus()
        if not sel:
            return
        v = tree.item(sel, "values")
        _clean()
        _editing_id[0] = int(v[0])
        cb_tipo.set(v[1])
        e_numdoc.insert(0, v[2])
        e_razon.insert(0, v[3])
        e_dir.insert(0, v[4])
        e_tel.insert(0, v[5])
        e_email.insert(0, v[6])

    def guardar():
        numdoc = e_numdoc.get().strip()
        razon = e_razon.get().strip()
        if not numdoc or not razon:
            messagebox.showwarning("Campos", "Nro. documento y razón social son obligatorios.")
            return
        try:
            svc.crear(cb_tipo.get(), numdoc, razon,
                      e_dir.get().strip(), e_tel.get().strip(), e_email.get().strip())
            _clean()
            cargar()
            messagebox.showinfo("OK", "Cliente guardado.")
        except Exception:
            messagebox.showerror("Error", "El número de documento ya existe.")

    def actualizar_cliente():
        if not _editing_id[0]:
            messagebox.showwarning("Selección", "Primero carga un cliente para editar.")
            return
        numdoc = e_numdoc.get().strip()
        razon = e_razon.get().strip()
        if not numdoc or not razon:
            messagebox.showwarning("Campos", "Nro. documento y razón social son obligatorios.")
            return
        svc.actualizar(_editing_id[0], cb_tipo.get(), numdoc, razon,
                       e_dir.get().strip(), e_tel.get().strip(), e_email.get().strip())
        _editing_id[0] = None
        _clean()
        cargar()
        messagebox.showinfo("OK", "Cliente actualizado.")

    def eliminar():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Elige un cliente.")
            return
        cid = int(tree.item(sel, "values")[0])
        nombre = tree.item(sel, "values")[3]
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre}?"):
            svc.eliminar(cid)
            cargar()
            messagebox.showinfo("OK", "Cliente eliminado.")

    # --- Botones ---
    acc = tk.Frame(frame, bg=BG)
    acc.grid(row=4, column=0, pady=(4, 8))
    for i, (txt, cmd) in enumerate([
        ("✏ Cargar para editar", _sel_to_inputs),
        ("✅ Actualizar", actualizar_cliente),
        ("🛑 Cancelar edición", lambda: (_clean(), _editing_id.__setitem__(0, None))),
        ("❌ Eliminar", eliminar),
        ("💾 Guardar Cliente", guardar),
    ]):
        tk.Button(acc, text=txt, command=cmd).grid(row=0, column=i, padx=5)

    tk.Button(frame, text="⬅ Volver", command=volver_funcion)\
        .grid(row=5, column=0, pady=(4, 12))
