# facturas_registro.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

FUENTE = ("Segoe UI", 10)
FUENTE_LBL = ("Segoe UI", 10)
BG = "#f8f8f8"

AFECTACIONES = ["Gravado", "Exonerado", "Inafecto"]
UNIDADES = ["UNIDAD", "UND", "MTR", "KG", "LT", "HORA", "SERV"]

def ventana_facturas_registro(frame_contenedor, volver_cb):
    # limpiar contenedor
    for w in frame_contenedor.winfo_children():
        w.destroy()
    frame_contenedor.pack_propagate(False)
    root = frame_contenedor.winfo_toplevel()

    # ======= CABECERA =======
    cabecera = tk.LabelFrame(frame_contenedor, text="", bg=BG, padx=10, pady=10)
    cabecera.pack(fill="x", padx=12, pady=(10, 8))
    cabecera.grid_columnconfigure(1, weight=1)

    tk.Label(cabecera, text="Número de documento", font=FUENTE_LBL, bg=BG)\
        .grid(row=0, column=0, sticky="e", padx=(0,8), pady=3)
    ent_ruc = tk.Entry(cabecera, font=FUENTE, width=28)
    ent_ruc.grid(row=0, column=1, sticky="w", pady=3)

    def simular_busqueda_sunat():
        r = ent_ruc.get().strip()
        if not r:
            messagebox.showwarning("RUC requerido", "Ingresa el RUC / DNI.")
            return
        ent_razon.config(state="normal"); ent_dir.config(state="normal")
        ent_razon.delete(0, "end"); ent_dir.delete(0, "end")
        ent_razon.insert(0, f"RAZÓN SOCIAL DEMO {r}")
        ent_dir.insert(0, "AV. DEMO 123 - HUANCAYO")
        ent_razon.config(state="readonly"); ent_dir.config(state="readonly")

    tk.Button(cabecera, text="Registrar", font=FUENTE, command=simular_busqueda_sunat)\
        .grid(row=0, column=2, sticky="w", padx=(8,0))

    tk.Label(cabecera, text="Razón Social", font=FUENTE_LBL, bg=BG)\
        .grid(row=1, column=0, sticky="e", padx=(0,8), pady=3)
    ent_razon = tk.Entry(cabecera, font=FUENTE, width=70, state="readonly")
    ent_razon.grid(row=1, column=1, columnspan=2, sticky="we", pady=3)

    tk.Label(cabecera, text="Dirección del Cliente", font=FUENTE_LBL, bg=BG)\
        .grid(row=2, column=0, sticky="e", padx=(0,8), pady=3)
    ent_dir = tk.Entry(cabecera, font=FUENTE, width=70, state="readonly")
    ent_dir.grid(row=2, column=1, columnspan=2, sticky="we", pady=3)

    tk.Label(cabecera, text="Tipo Moneda", font=FUENTE_LBL, bg=BG)\
        .grid(row=3, column=0, sticky="e", padx=(0,8), pady=3)
    cb_moneda = ttk.Combobox(cabecera, values=["SOLES", "DÓLARES"], state="readonly", width=20)
    cb_moneda.set("SOLES")
    cb_moneda.grid(row=3, column=1, sticky="w", pady=3)

    tk.Label(cabecera, text="Fecha de Emisión", font=FUENTE_LBL, bg=BG)\
        .grid(row=3, column=2, sticky="e", padx=(12,6))
    ent_fecha = tk.Entry(cabecera, font=FUENTE, width=12)
    ent_fecha.insert(0, date.today().isoformat())
    ent_fecha.grid(row=3, column=3, sticky="w")

    # ======= DETALLE + TOTALES =======
    cuerpo = tk.Frame(frame_contenedor, bg=BG)
    cuerpo.pack(fill="both", expand=True, padx=12)
    cuerpo.grid_columnconfigure(0, weight=1)
    cuerpo.grid_rowconfigure(1, weight=1)

    barra = tk.Frame(cuerpo, bg=BG)
    barra.grid(row=0, column=0, sticky="we")
    btn_add = tk.Button(barra, text="➕ Adicionar", font=FUENTE)
    btn_edit = tk.Button(barra, text="✏️ Editar", font=FUENTE)
    btn_del = tk.Button(barra, text="🗑 Eliminar", font=FUENTE)
    btn_add.pack(side="left", padx=(0,6)); btn_edit.pack(side="left", padx=6); btn_del.pack(side="left", padx=6)

    cols = ("Bien/Servicio", "Afectación", "Unidad", "Cantidad", "Código", "Descripción", "Valor Unit.", "Subtotal", "IGV", "ISC", "ICBPER", "Total")
    tree = ttk.Treeview(cuerpo, columns=cols, show="headings", height=10)
    for c in cols:
        tree.heading(c, text=c)
    widths = [140, 120, 90, 80, 100, 280, 100, 100, 80, 80, 80, 110]
    anchors = ["w","center","center","center","w","w","e","e","e","e","e","e"]
    for c, w, a in zip(cols, widths, anchors):
        tree.column(c, width=w, anchor=a)
    tree.grid(row=1, column=0, sticky="nsew", pady=(4,6))

    sy = ttk.Scrollbar(cuerpo, orient="vertical", command=tree.yview)
    tree.configure(yscroll=sy.set)
    sy.grid(row=1, column=1, sticky="ns")

    panel_tot = tk.Frame(cuerpo, bg=BG, bd=1, relief="solid")
    panel_tot.grid(row=0, column=2, rowspan=2, sticky="n", padx=(10,0), pady=(0,6))

    def fila_total(r, texto, var):
        tk.Label(panel_tot, text=texto, font=FUENTE_LBL, bg=BG)\
          .grid(row=r, column=0, sticky="e", padx=(6,6), pady=3)
        tk.Entry(panel_tot, textvariable=var, font=FUENTE, width=16, state="readonly", justify="right")\
          .grid(row=r, column=1, sticky="w", padx=(0,6))

    subtotal_var = tk.StringVar(value="0.00")
    anticipos_var = tk.StringVar(value="0.00")
    descuentos_var = tk.StringVar(value="0.00")
    valor_venta_var = tk.StringVar(value="0.00")
    isc_var = tk.StringVar(value="0.00")
    igv_var = tk.StringVar(value="0.00")
    icbper_var = tk.StringVar(value="0.00")
    otros_cargos_var = tk.StringVar(value="0.00")
    otros_trib_var = tk.StringVar(value="0.00")
    redondeo_var = tk.StringVar(value="0.00")
    total_var = tk.StringVar(value="0.00")

    labels = [
        ("Sub Total Ventas", subtotal_var),
        ("Anticipos", anticipos_var),
        ("Descuentos", descuentos_var),
        ("Valor de Venta", valor_venta_var),
        ("ISC", isc_var),
        ("IGV", igv_var),
        ("ICBPER", icbper_var),
        ("Otros Cargos", otros_cargos_var),
        ("Otros Tributos", otros_trib_var),
        ("Monto de Redondeo", redondeo_var),
        ("Importe Total", total_var),
    ]
    for i, (t, v) in enumerate(labels):
        fila_total(i, t + " : ", v)

    # ======= DATOS ÍTEMS + TOTALES =======
    items = []  # cada item: dict con base(subtotal), igv, isc, icbper, total ...

    def recalcular_totales():
        base = sum(i["subtotal"] for i in items)
        igv_sum = sum(i["igv"] for i in items)
        isc_sum = sum(i["isc"] for i in items)
        icb_sum = sum(i["icbper"] for i in items)
        desc = float(descuentos_var.get() or 0)
        ant = float(anticipos_var.get() or 0)
        otros_c = float(otros_cargos_var.get() or 0)
        otros_t = float(otros_trib_var.get() or 0)
        red = float(redondeo_var.get() or 0)

        valor_venta = max(base - desc - ant, 0)
        total_calc = valor_venta + igv_sum + isc_sum + icb_sum + otros_c + otros_t + red

        subtotal_var.set(f"{base:.2f}")
        valor_venta_var.set(f"{valor_venta:.2f}")
        igv_var.set(f"{igv_sum:.2f}")
        isc_var.set(f"{isc_sum:.2f}")
        icbper_var.set(f"{icb_sum:.2f}")
        total_var.set(f"{total_calc:.2f}")

    # ======= MODAL DE ÍTEM (formato de tu captura) =======
    def abrir_modal_item(edit=False):
        win = tk.Toplevel(root)
        win.title("Editar ítem" if edit else "Adicionar ítem")
        win.transient(root); win.grab_set()
        win.configure(bg=BG)
        pad = dict(padx=6, pady=3)

        # Bien/Servicio
        tipo_var = tk.StringVar(value="Bien")
        tk.Radiobutton(win, text="Bien", variable=tipo_var, value="Bien", bg=BG).grid(row=0, column=0, sticky="w", **pad)
        tk.Radiobutton(win, text="Servicio", variable=tipo_var, value="Servicio", bg=BG).grid(row=0, column=1, sticky="w", **pad)

        # Cantidad
        tk.Label(win, text="Cantidad", bg=BG).grid(row=1, column=0, sticky="e", **pad)
        e_cant = tk.Entry(win, width=14); e_cant.insert(0, "1")
        e_cant.grid(row=1, column=1, sticky="w", **pad)

        # Unidad
        tk.Label(win, text="Unidad de Medida", bg=BG).grid(row=2, column=0, sticky="e", **pad)
        cb_un = ttk.Combobox(win, values=UNIDADES, state="readonly", width=20)
        cb_un.set("UNIDAD")
        cb_un.grid(row=2, column=1, sticky="w", **pad)

        # Código
        tk.Label(win, text="Código", bg=BG).grid(row=3, column=0, sticky="e", **pad)
        e_cod = tk.Entry(win, width=30)
        e_cod.grid(row=3, column=1, sticky="w", **pad)

        # Descripción (multilínea)
        tk.Label(win, text="Descripción", bg=BG).grid(row=4, column=0, sticky="ne", **pad)
        txt_desc = tk.Text(win, width=46, height=4)
        txt_desc.grid(row=4, column=1, sticky="w", **pad)

        # Bolsas plásticas (ICBPER)
        tk.Label(win, text="Impuesto Bolsas Plásticas", bg=BG).grid(row=5, column=0, sticky="e", **pad)
        icb_si_no = tk.StringVar(value="NO")
        tk.Radiobutton(win, text="SI", variable=icb_si_no, value="SI", bg=BG).grid(row=5, column=1, sticky="w", **pad)
        tk.Radiobutton(win, text="NO", variable=icb_si_no, value="NO", bg=BG).grid(row=5, column=1, sticky="e", **pad)

        # Valor unitario
        tk.Label(win, text="Valor Unitario", bg=BG).grid(row=6, column=0, sticky="e", **pad)
        e_val = tk.Entry(win, width=18); e_val.insert(0, "0.00")
        e_val.grid(row=6, column=1, sticky="w", **pad)

        # Descuento (monto)
        tk.Label(win, text="Descuento", bg=BG).grid(row=7, column=0, sticky="e", **pad)
        e_desc = tk.Entry(win, width=18); e_desc.insert(0, "0.00")
        e_desc.grid(row=7, column=1, sticky="w", **pad)

        # ISC (monto)
        tk.Label(win, text="ISC", bg=BG).grid(row=8, column=0, sticky="e", **pad)
        e_isc = tk.Entry(win, width=18); e_isc.insert(0, "0.00")
        e_isc.grid(row=8, column=1, sticky="w", **pad)

        # IGV % (18 o 10) y afectación
        tk.Label(win, text="IGV", bg=BG).grid(row=9, column=0, sticky="e", **pad)
        igv_rate = tk.DoubleVar(value=0.18)
        tk.Radiobutton(win, text="18 %", variable=igv_rate, value=0.18, bg=BG)\
            .grid(row=9, column=1, sticky="w", **pad)
        tk.Radiobutton(win, text="10 %", variable=igv_rate, value=0.10, bg=BG)\
            .grid(row=9, column=1, sticky="e", **pad)

        tk.Label(win, text="", bg=BG).grid(row=10, column=0)  # separador visual

        afect_var = tk.StringVar(value="Gravado")
        fila_af = 11
        tk.Radiobutton(win, text="Gravado", variable=afect_var, value="Gravado", bg=BG).grid(row=fila_af, column=1, sticky="w", **pad)
        tk.Radiobutton(win, text="Exonerado", variable=afect_var, value="Exonerado", bg=BG).grid(row=fila_af, column=1, sticky="e", **pad)
        tk.Radiobutton(win, text="Inafecto", variable=afect_var, value="Inafecto", bg=BG).grid(row=fila_af, column=1, sticky="ne", padx=(140,6), pady=3)

        # Importe ICBPER y Total item (readonly)
        tk.Label(win, text="Impuesto ICBPER", bg=BG).grid(row=12, column=0, sticky="e", **pad)
        e_icbper = tk.Entry(win, width=18, state="readonly")
        e_icbper.grid(row=12, column=1, sticky="w", **pad)

        tk.Label(win, text="Importe Total del Ítem", bg=BG).grid(row=13, column=0, sticky="e", **pad)
        e_total_item = tk.Entry(win, width=18, state="readonly")
        e_total_item.grid(row=13, column=1, sticky="w", **pad)

        def icbper_tarifa():
            # Tarifa de bolsa (S/ 0.50 por unidad como ejemplo); ajusta si lo deseas
            try:
                cant = float(e_cant.get() or "0")
            except ValueError:
                cant = 0
            return round(0.50 * cant, 2) if icb_si_no.get() == "SI" else 0.0

        def recalcular_item(*_):
            try:
                cant = float(e_cant.get() or "0")
                vu = float(e_val.get() or "0")
                desc = float(e_desc.get() or "0")
                isc = float(e_isc.get() or "0")
            except ValueError:
                return
            base = max(cant * vu - desc, 0)
            icb = icbper_tarifa()
            igv = round(base * igv_rate.get(), 2) if afect_var.get() == "Gravado" else 0.0
            total_item = base + igv + isc + icb
            e_icbper.config(state="normal"); e_icbper.delete(0, "end"); e_icbper.insert(0, f"{icb:.2f}"); e_icbper.config(state="readonly")
            e_total_item.config(state="normal"); e_total_item.delete(0, "end"); e_total_item.insert(0, f"{total_item:.2f}"); e_total_item.config(state="readonly")

        # Bind para recalcular en tiempo real
        for w in (e_cant, e_val, e_desc, e_isc):
            w.bind("<KeyRelease>", recalcular_item)
        for rb in (win,):
            # simples cambios de selección
            pass
        def on_change_afect(*_): recalcular_item()
        def on_change_icb(*_):   recalcular_item()
        def on_change_rate(*_):  recalcular_item()
        afect_var.trace_add("write", on_change_afect)
        icb_si_no.trace_add("write", on_change_icb)
        igv_rate.trace_add("write", on_change_rate)

        # Cargar datos si es edición
        idx_edit = None
        if edit:
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Editar", "Selecciona un ítem.")
                win.destroy(); return
            idx_edit = tree.index(sel[0])
            it = items[idx_edit]
            tipo_var.set(it.get("tipo","Bien"))
            e_cant.delete(0, "end"); e_cant.insert(0, str(it["cantidad"]))
            cb_un.set(it["unidad"])
            e_cod.insert(0, it["codigo"])
            txt_desc.insert("1.0", it["descripcion"])
            icb_si_no.set("SI" if it["icbper"] > 0 else "NO")
            e_val.delete(0, "end"); e_val.insert(0, f"{it['valor_unit']:.2f}")
            e_desc.delete(0, "end"); e_desc.insert(0, f"{it.get('descuento',0.0):.2f}")
            e_isc.delete(0, "end"); e_isc.insert(0, f"{it.get('isc',0.0):.2f}")
            igv_rate.set(it.get("igv_rate",0.18))
            afect_var.set(it["afectacion"])
            recalcular_item()

        # Botones
        def aceptar():
            try:
                cant = float(e_cant.get() or "0")
                vu = float(e_val.get() or "0")
                desc = float(e_desc.get() or "0")
                isc = float(e_isc.get() or "0")
            except ValueError:
                messagebox.showerror("Dato inválido", "Revisa cantidades y montos.")
                return

            bien = tipo_var.get()
            unidad = cb_un.get()
            codigo = e_cod.get().strip()
            desc_txt = txt_desc.get("1.0", "end").strip()
            afect = afect_var.get()
            base = max(cant * vu - desc, 0)
            icb = icbper_tarifa()
            igv_m = round(base * igv_rate.get(), 2) if afect == "Gravado" else 0.0
            total_i = base + igv_m + isc + icb

            data = dict(
                tipo=bien, unidad=unidad, codigo=codigo, descripcion=desc_txt,
                afectacion=afect, cantidad=cant, valor_unit=vu,
                descuento=desc, subtotal=base, igv=igv_m, igv_rate=igv_rate.get(),
                isc=isc, icbper=icb, total=total_i
            )

            if not desc_txt:
                messagebox.showwarning("Faltan datos", "Ingresa la descripción.")
                return

            vals_row = (bien, afect, unidad, f"{cant:g}", codigo, desc_txt,
                        f"{vu:.2f}", f"{base:.2f}", f"{igv_m:.2f}", f"{isc:.2f}", f"{icb:.2f}", f"{total_i:.2f}")

            if edit:
                items[idx_edit] = data
                iid = tree.get_children()[idx_edit]
                tree.item(iid, values=vals_row)
            else:
                items.append(data)
                tree.insert("", "end", values=vals_row)

            win.destroy()
            recalcular_totales()

        tk.Frame(win, height=8, bg=BG).grid(row=14, column=0)  # separador
        tk.Button(win, text="✔ Aceptar", width=12, command=aceptar).grid(row=15, column=0, pady=8)
        tk.Button(win, text="✖ Cancelar", width=12, command=win.destroy).grid(row=15, column=1, pady=8, sticky="w")

        recalcular_item()
        win.wait_window()

    def eliminar_sel():
        sel = tree.selection()
        if not sel:
            return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el ítem seleccionado?"):
            return
        idx = tree.index(sel[0])
        tree.delete(sel[0])
        try:
            items.pop(idx)
        except Exception:
            pass
        recalcular_totales()

    btn_add.config(command=lambda: abrir_modal_item(False))
    btn_edit.config(command=lambda: abrir_modal_item(True))
    btn_del.config(command=eliminar_sel)

    # ======= BOTONERA =======
    pie = tk.Frame(frame_contenedor, bg=BG)
    pie.pack(fill="x", padx=12, pady=(4, 12))

    def continuar():
        if not items:
            messagebox.showwarning("Sin ítems", "Agrega al menos un ítem.")
            return
        messagebox.showinfo("Continuar", "Luego aquí haremos la vista previa / PDF.")

    tk.Button(pie, text="◀ Retroceder", font=FUENTE, command=volver_cb).pack(side="left", padx=6)
    tk.Button(pie, text="▶ Continuar", font=FUENTE, command=continuar).pack(side="left", padx=6)
    tk.Button(pie, text="✖ Cancelar", font=FUENTE, command=volver_cb).pack(side="left", padx=6)
