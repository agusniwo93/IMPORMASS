# src/impormass/ui/ver_facturas.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import factura_service as fac_svc
from ..utils.ui_helpers import auto_resize_treeview

BG = "#f8f8f8"


def vista_ver_facturas(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="FACTURAS EMITIDAS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(14, 8), sticky="n")

    # --- Contenido ---
    content = tk.Frame(frame, bg=BG)
    content.grid(row=1, column=0, sticky="nsew", padx=12)
    content.rowconfigure(1, weight=1)
    content.columnconfigure(0, weight=1)

    # Barra búsqueda
    barra = tk.Frame(content, bg=BG)
    barra.grid(row=0, column=0, sticky="ew", pady=(0, 6))
    barra.columnconfigure(1, weight=1)
    tk.Label(barra, text="🔍 Buscar:", bg=BG).grid(row=0, column=0, padx=(0, 6))
    e_buscar = tk.Entry(barra, font=("Segoe UI", 12))
    e_buscar.grid(row=0, column=1, sticky="ew")

    # Tabla facturas
    wrap = tk.Frame(content)
    wrap.grid(row=1, column=0, sticky="nsew", pady=6)
    wrap.rowconfigure(0, weight=1)
    wrap.columnconfigure(0, weight=1)

    cols = ("ID", "Nro. Factura", "Cliente", "Fecha", "Moneda", "Total", "Estado")
    tree = ttk.Treeview(wrap, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
    tree.column("ID", width=40)
    tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(tree, fractions=[0.05, 0.15, 0.25, 0.12, 0.10, 0.13, 0.10])

    sy = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
    tree.configure(yscroll=sy.set)
    sy.grid(row=0, column=1, sticky="ns")

    def cargar(f=""):
        tree.delete(*tree.get_children())
        for fila in fac_svc.listar(f):
            tree.insert("", tk.END, values=fila)

    e_buscar.bind("<KeyRelease>", lambda e: cargar(e_buscar.get()))
    cargar()

    # --- Detalle ---
    det_frame = tk.LabelFrame(content, text="Detalle de Factura", bg=BG, padx=8, pady=8)
    det_frame.grid(row=2, column=0, sticky="ew", pady=(6, 4))
    det_frame.columnconfigure(0, weight=1)

    det_cols = ("Tipo", "Afectación", "Unidad", "Cant.", "Código",
                "Descripción", "V.Unit.", "Desc.", "Subtotal", "IGV", "ISC", "ICBPER", "Total")
    det_tree = ttk.Treeview(det_frame, columns=det_cols, show="headings", height=5)
    for c in det_cols:
        det_tree.heading(c, text=c)
    det_tree.grid(row=0, column=0, sticky="ew")
    auto_resize_treeview(det_tree, fractions=[0.07, 0.08, 0.06, 0.05, 0.07,
                                               0.18, 0.07, 0.06, 0.08, 0.07, 0.06, 0.06, 0.09])

    def mostrar_detalle(_e=None):
        det_tree.delete(*det_tree.get_children())
        sel = tree.focus()
        if not sel:
            return
        fac_id = int(tree.item(sel, "values")[0])
        for fila in fac_svc.obtener_detalle(fac_id):
            det_tree.insert("", tk.END, values=fila)

    tree.bind("<<TreeviewSelect>>", mostrar_detalle)

    # --- Botones ---
    acc = tk.Frame(content, bg=BG)
    acc.grid(row=3, column=0, pady=(4, 4))

    def anular_factura():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona una factura.")
            return
        vals = tree.item(sel, "values")
        fac_id = int(vals[0])
        estado = vals[6]
        if estado == "ANULADA":
            messagebox.showinfo("Info", "La factura ya está anulada.")
            return
        if messagebox.askyesno("Confirmar", f"¿Anular factura {vals[1]}?"):
            fac_svc.anular(fac_id)
            cargar(e_buscar.get())
            messagebox.showinfo("OK", "Factura anulada.")

    tk.Button(acc, text="🚫 Anular Factura", command=anular_factura).grid(row=0, column=0, padx=5)

    tk.Button(frame, text="⬅ Volver", command=volver_funcion)\
        .grid(row=2, column=0, pady=(4, 12))
