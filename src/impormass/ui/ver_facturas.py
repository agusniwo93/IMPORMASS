# src/impormass/ui/ver_facturas.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import factura_service as fac_svc
from ..utils.ui_helpers import auto_resize_treeview

BG = "#f8f8f8"


def vista_ver_facturas(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    # Layout: título(0), búsqueda(1), tabla facturas(2), info+detalle(3), botones(4), volver(5)
    for i in range(6):
        frame.rowconfigure(i, weight=0)
    frame.rowconfigure(2, weight=3)   # tabla principal crece más
    frame.rowconfigure(3, weight=2)   # detalle también crece
    frame.columnconfigure(0, weight=1)

    # --- Título ---
    tk.Label(frame, text="FACTURAS EMITIDAS",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(10, 6), sticky="n")

    # --- Barra búsqueda ---
    barra = tk.Frame(frame, bg=BG)
    barra.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 4))
    barra.columnconfigure(1, weight=1)
    tk.Label(barra, text="Buscar:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=0, column=0, padx=(0, 6))
    e_buscar = tk.Entry(barra, font=("Segoe UI", 11))
    e_buscar.grid(row=0, column=1, sticky="ew")

    # --- Tabla facturas ---
    wrap = tk.Frame(frame)
    wrap.grid(row=2, column=0, sticky="nsew", padx=12, pady=4)
    wrap.rowconfigure(0, weight=1)
    wrap.columnconfigure(0, weight=1)

    cols = ("ID", "Nro. Factura", "Cliente", "Fecha", "Moneda", "Total", "Estado")
    tree = ttk.Treeview(wrap, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
    tree.column("ID", width=40, minwidth=30)
    tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(tree, fractions=[0.05, 0.15, 0.28, 0.12, 0.10, 0.13, 0.10])

    sy = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
    sx = ttk.Scrollbar(wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=sy.set, xscroll=sx.set)
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")

    def cargar(f=""):
        tree.delete(*tree.get_children())
        for fila in fac_svc.listar(f):
            tree.insert("", tk.END, values=fila)

    e_buscar.bind("<KeyRelease>", lambda e: cargar(e_buscar.get()))
    cargar()

    # --- Panel información + detalle ---
    info_det = tk.Frame(frame, bg=BG)
    info_det.grid(row=3, column=0, sticky="nsew", padx=12, pady=(2, 4))
    info_det.rowconfigure(0, weight=1)
    info_det.columnconfigure(0, weight=0)
    info_det.columnconfigure(1, weight=1)

    # Sub-panel info de la factura seleccionada
    info_frame = tk.LabelFrame(info_det, text="Información de Factura",
                                bg=BG, padx=8, pady=6, font=("Segoe UI", 9, "bold"))
    info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

    info_labels = {}
    campos_info = [
        ("Nro. Factura:", "nro"),
        ("Cliente:", "cliente"),
        ("Documento:", "documento"),
        ("Dirección:", "direccion"),
        ("Fecha:", "fecha"),
        ("Moneda:", "moneda"),
        ("Subtotal:", "subtotal"),
        ("Descuentos:", "descuentos"),
        ("IGV:", "igv"),
        ("ISC:", "isc"),
        ("ICBPER:", "icbper"),
        ("Total:", "total"),
        ("Estado:", "estado"),
    ]
    for i, (texto, key) in enumerate(campos_info):
        tk.Label(info_frame, text=texto, bg=BG, font=("Segoe UI", 9, "bold"),
                 anchor="e", width=12)\
            .grid(row=i, column=0, sticky="e", padx=(2, 4), pady=1)
        lbl = tk.Label(info_frame, text="—", bg=BG, font=("Segoe UI", 9),
                       anchor="w")
        lbl.grid(row=i, column=1, sticky="w", padx=(0, 6), pady=1)
        info_labels[key] = lbl

    # Sub-panel detalle de ítems
    det_frame = tk.LabelFrame(info_det, text="Detalle de Ítems",
                               bg=BG, padx=6, pady=6, font=("Segoe UI", 9, "bold"))
    det_frame.grid(row=0, column=1, sticky="nsew")
    det_frame.rowconfigure(0, weight=1)
    det_frame.columnconfigure(0, weight=1)

    det_cols = ("Tipo", "Afectación", "Unidad", "Cant.", "Código",
                "Descripción", "V.Unit.", "Desc.", "Subtotal", "IGV", "ISC", "ICBPER", "Total")
    det_tree = ttk.Treeview(det_frame, columns=det_cols, show="headings", height=5)
    for c in det_cols:
        det_tree.heading(c, text=c)
    det_tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(det_tree, fractions=[0.07, 0.08, 0.06, 0.05, 0.07,
                                               0.18, 0.07, 0.06, 0.08, 0.07, 0.06, 0.06, 0.09])

    det_sy = ttk.Scrollbar(det_frame, orient="vertical", command=det_tree.yview)
    det_sx = ttk.Scrollbar(det_frame, orient="horizontal", command=det_tree.xview)
    det_tree.configure(yscroll=det_sy.set, xscroll=det_sx.set)
    det_sy.grid(row=0, column=1, sticky="ns")
    det_sx.grid(row=1, column=0, sticky="ew")

    def mostrar_detalle(_e=None):
        det_tree.delete(*det_tree.get_children())
        sel = tree.focus()
        if not sel:
            for lbl in info_labels.values():
                lbl.config(text="—")
            return

        fac_id = int(tree.item(sel, "values")[0])

        # Cargar info completa de la factura
        fac = fac_svc.obtener(fac_id)
        if fac:
            # fac = (id, serie, numero, cliente_id, moneda, fecha, subtotal,
            #        descuentos, valor_venta, igv, isc, icbper, otros_cargos, total, estado,
            #        razon_social, num_doc, direccion)
            info_labels["nro"].config(text=f"{fac[1]}-{fac[2]:08d}")
            info_labels["cliente"].config(text=fac[15] or "—")
            info_labels["documento"].config(text=fac[16] or "—")
            info_labels["direccion"].config(text=fac[17] or "—")
            info_labels["fecha"].config(text=fac[5] or "—")
            info_labels["moneda"].config(text=fac[4] or "—")
            info_labels["subtotal"].config(text=f"S/. {fac[6]:.2f}")
            info_labels["descuentos"].config(text=f"S/. {fac[7]:.2f}")
            info_labels["igv"].config(text=f"S/. {fac[9]:.2f}")
            info_labels["isc"].config(text=f"S/. {fac[10]:.2f}")
            info_labels["icbper"].config(text=f"S/. {fac[11]:.2f}")
            info_labels["total"].config(text=f"S/. {fac[13]:.2f}")
            estado = fac[14]
            color = "#cc0000" if estado == "ANULADA" else "#007a00"
            info_labels["estado"].config(text=estado, fg=color)

        # Cargar detalle de ítems
        for fila in fac_svc.obtener_detalle(fac_id):
            det_tree.insert("", tk.END, values=fila)

    tree.bind("<<TreeviewSelect>>", mostrar_detalle)

    # --- Botones de acción ---
    acc = tk.Frame(frame, bg=BG)
    acc.grid(row=4, column=0, pady=(4, 2))

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

    tk.Button(acc, text="Anular Factura", font=("Segoe UI", 10),
              bg="#cc3333", fg="white", activebackground="#aa1111",
              command=anular_factura)\
        .grid(row=0, column=0, padx=8)

    tk.Button(acc, text="Actualizar Lista", font=("Segoe UI", 10),
              command=lambda: cargar(e_buscar.get()))\
        .grid(row=0, column=1, padx=8)

    # --- Botón volver (prominente) ---
    tk.Button(frame, text="Volver al Menu Principal", font=("Segoe UI", 11, "bold"),
              command=volver_funcion, bg="#007acc", fg="white",
              activebackground="#005f99", relief="flat", padx=16, pady=4)\
        .grid(row=5, column=0, pady=(4, 10))
