# src/impormass/ui/facturas.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from ..utils.ui_helpers import auto_resize_treeview
from ..services import cliente_service as cli_svc
from ..services import producto_service as prod_svc
from ..services import factura_service as fac_svc
from ..services import config_service as cfg_svc

FUENTE = ("Segoe UI", 10)
FUENTE_LBL = ("Segoe UI", 10)
BG = "#f8f8f8"

AFECTACIONES = ["Gravado", "Exonerado", "Inafecto"]
UNIDADES = ["UNIDAD", "UND", "MTR", "KG", "LT", "HORA", "SERV"]

def ventana_facturas_registro(frame_contenedor, volver_cb):
    for w in frame_contenedor.winfo_children(): w.destroy()
    frame_contenedor.rowconfigure(0, weight=0)
    frame_contenedor.rowconfigure(1, weight=1)
    frame_contenedor.rowconfigure(2, weight=0)
    frame_contenedor.columnconfigure(0, weight=1)

    root = frame_contenedor.winfo_toplevel()
    cliente_actual = [None]  # [id] del cliente seleccionado

    # ======= CABECERA =======
    cabecera = tk.LabelFrame(frame_contenedor, text="Datos del Comprobante", bg=BG, padx=10, pady=6)
    cabecera.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 4))
    cabecera.columnconfigure(1, weight=1)
    cabecera.columnconfigure(3, weight=0)

    tk.Label(cabecera, text="Número de documento", font=FUENTE_LBL, bg=BG)\
        .grid(row=0, column=0, sticky="e", padx=(0,8), pady=3)
    ent_ruc = tk.Entry(cabecera, font=FUENTE, width=28)
    ent_ruc.grid(row=0, column=1, sticky="w", pady=3)

    def buscar_cliente():
        r = ent_ruc.get().strip()
        if not r:
            messagebox.showwarning("Documento requerido", "Ingresa el RUC / DNI."); return
        cl = cli_svc.buscar_por_documento(r)
        if cl:
            cliente_actual[0] = cl[0]  # id
            ent_razon.config(state="normal"); ent_dir.config(state="normal")
            ent_razon.delete(0,"end"); ent_dir.delete(0,"end")
            ent_razon.insert(0, cl[3])  # razon_social
            ent_dir.insert(0, cl[4] or "")  # direccion
            ent_razon.config(state="readonly"); ent_dir.config(state="readonly")
        else:
            if messagebox.askyesno("Cliente no encontrado",
                                   f"No se encontró el documento {r}.\n¿Desea registrarlo ahora?"):
                _registrar_cliente_rapido(r)

    def _registrar_cliente_rapido(num_doc):
        win = tk.Toplevel(root)
        win.title("Registrar Cliente Rápido")
        win.transient(root); win.grab_set(); win.configure(bg=BG)
        pad = dict(padx=6, pady=4)

        tk.Label(win, text="Tipo Doc.", bg=BG).grid(row=0, column=0, sticky="e", **pad)
        cb_t = ttk.Combobox(win, values=["RUC", "DNI", "CE"], state="readonly", width=8)
        cb_t.set("RUC" if len(num_doc) == 11 else "DNI")
        cb_t.grid(row=0, column=1, sticky="w", **pad)

        tk.Label(win, text="Nro. Documento", bg=BG).grid(row=1, column=0, sticky="e", **pad)
        e_nd = tk.Entry(win, width=20); e_nd.insert(0, num_doc)
        e_nd.grid(row=1, column=1, sticky="w", **pad)

        tk.Label(win, text="Razón Social", bg=BG).grid(row=2, column=0, sticky="e", **pad)
        e_rs = tk.Entry(win, width=40); e_rs.grid(row=2, column=1, sticky="ew", **pad)

        tk.Label(win, text="Dirección", bg=BG).grid(row=3, column=0, sticky="e", **pad)
        e_dir2 = tk.Entry(win, width=40); e_dir2.grid(row=3, column=1, sticky="ew", **pad)

        def guardar_cli():
            rs = e_rs.get().strip()
            nd = e_nd.get().strip()
            if not rs or not nd:
                messagebox.showwarning("Campos", "Razón social y documento son obligatorios."); return
            try:
                cid = cli_svc.crear(cb_t.get(), nd, rs, e_dir2.get().strip())
                cliente_actual[0] = cid
                ent_razon.config(state="normal"); ent_dir.config(state="normal")
                ent_razon.delete(0,"end"); ent_dir.delete(0,"end")
                ent_razon.insert(0, rs)
                ent_dir.insert(0, e_dir2.get().strip())
                ent_razon.config(state="readonly"); ent_dir.config(state="readonly")
                win.destroy()
            except Exception:
                messagebox.showerror("Error", "No se pudo registrar. Documento duplicado?")

        tk.Button(win, text="💾 Guardar", command=guardar_cli).grid(row=4, column=1, sticky="e", **pad)

    tk.Button(cabecera, text="Buscar", font=FUENTE, command=buscar_cliente)\
        .grid(row=0, column=2, sticky="w", padx=(8,0))

    tk.Label(cabecera, text="Razón Social", font=FUENTE_LBL, bg=BG)\
        .grid(row=1, column=0, sticky="e", padx=(0,8), pady=3)
    ent_razon = tk.Entry(cabecera, font=FUENTE, state="readonly")
    ent_razon.grid(row=1, column=1, columnspan=2, sticky="ew", pady=3)

    tk.Label(cabecera, text="Dirección del Cliente", font=FUENTE_LBL, bg=BG)\
        .grid(row=2, column=0, sticky="e", padx=(0,8), pady=3)
    ent_dir = tk.Entry(cabecera, font=FUENTE, state="readonly")
    ent_dir.grid(row=2, column=1, columnspan=2, sticky="ew", pady=3)

    tk.Label(cabecera, text="Tipo Moneda", font=FUENTE_LBL, bg=BG)\
        .grid(row=3, column=0, sticky="e", padx=(0,8), pady=3)
    moneda_def = cfg_svc.obtener("moneda_defecto") or "SOLES"
    cb_moneda = ttk.Combobox(cabecera, values=["SOLES", "DOLARES"], state="readonly", width=20)
    cb_moneda.set(moneda_def)
    cb_moneda.grid(row=3, column=1, sticky="w", pady=3)

    tk.Label(cabecera, text="Fecha de Emisión", font=FUENTE_LBL, bg=BG)\
        .grid(row=3, column=2, sticky="e", padx=(12,6))
    ent_fecha = tk.Entry(cabecera, font=FUENTE, width=12)
    ent_fecha.insert(0, date.today().isoformat())
    ent_fecha.grid(row=3, column=3, sticky="w")

    # ======= CUERPO (detalle + totales) =======
    cuerpo = tk.Frame(frame_contenedor, bg=BG)
    cuerpo.grid(row=1, column=0, sticky="nsew", padx=12)
    cuerpo.rowconfigure(1, weight=1)
    cuerpo.rowconfigure(2, weight=0)
    cuerpo.columnconfigure(0, weight=1)

    # barra acciones
    barra = tk.Frame(cuerpo, bg=BG)
    barra.grid(row=0, column=0, sticky="ew")
    btn_add = tk.Button(barra, text="Adicionar", font=FUENTE)
    btn_edit = tk.Button(barra, text="Editar", font=FUENTE)
    btn_del = tk.Button(barra, text="Eliminar", font=FUENTE)
    for i, b in enumerate((btn_add, btn_edit, btn_del)):
        b.grid(row=0, column=i, padx=6, pady=2)

    # tabla
    cols = ("Bien/Servicio", "Afectacion", "Unidad", "Cantidad", "Codigo",
            "Descripcion", "Valor Unit.", "Subtotal", "IGV", "ISC", "ICBPER", "Total")
    tabla_wrap = tk.Frame(cuerpo, bg=BG)
    tabla_wrap.grid(row=1, column=0, sticky="nsew", pady=(4, 4))
    tabla_wrap.rowconfigure(0, weight=1)
    tabla_wrap.columnconfigure(0, weight=1)

    tree = ttk.Treeview(tabla_wrap, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
    tree.grid(row=0, column=0, sticky="nsew")
    auto_resize_treeview(tree, fractions=[0.09, 0.08, 0.06, 0.06, 0.08, 0.18, 0.08, 0.08, 0.07, 0.06, 0.06, 0.10])

    sy = ttk.Scrollbar(tabla_wrap, orient="vertical", command=tree.yview)
    sx = ttk.Scrollbar(tabla_wrap, orient="horizontal", command=tree.xview)
    tree.configure(yscroll=sy.set, xscroll=sx.set)
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")

    # panel totales - horizontal debajo de la tabla para mejor responsividad
    panel_tot = tk.LabelFrame(cuerpo, text="Totales", bg=BG, padx=6, pady=4)
    panel_tot.grid(row=2, column=0, sticky="ew", pady=(2, 4))

    subtotal_var   = tk.StringVar(value="0.00")
    anticipos_var  = tk.StringVar(value="0.00")
    descuentos_var = tk.StringVar(value="0.00")
    valor_venta_var= tk.StringVar(value="0.00")
    isc_var        = tk.StringVar(value="0.00")
    igv_var        = tk.StringVar(value="0.00")
    icbper_var     = tk.StringVar(value="0.00")
    otros_cargos_var = tk.StringVar(value="0.00")
    otros_trib_var   = tk.StringVar(value="0.00")
    redondeo_var     = tk.StringVar(value="0.00")
    total_var        = tk.StringVar(value="0.00")

    # Fila superior de totales
    labels_row1 = [
        ("SubTotal", subtotal_var),
        ("Descuentos", descuentos_var),
        ("Valor Venta", valor_venta_var),
        ("IGV", igv_var),
        ("ISC", isc_var),
        ("ICBPER", icbper_var),
    ]
    labels_row2 = [
        ("Anticipos", anticipos_var),
        ("Otros Cargos", otros_cargos_var),
        ("Otros Tributos", otros_trib_var),
        ("Redondeo", redondeo_var),
        ("TOTAL", total_var),
    ]

    for col_idx, (texto, var) in enumerate(labels_row1):
        panel_tot.columnconfigure(col_idx, weight=1)
        tk.Label(panel_tot, text=texto, font=("Segoe UI", 8), bg=BG)\
            .grid(row=0, column=col_idx, padx=2, pady=(0, 1))
        tk.Entry(panel_tot, textvariable=var, font=("Segoe UI", 9),
                 width=12, state="readonly", justify="right")\
            .grid(row=1, column=col_idx, padx=2, pady=(0, 2), sticky="ew")

    for col_idx, (texto, var) in enumerate(labels_row2):
        f = ("Segoe UI", 9, "bold") if texto == "TOTAL" else ("Segoe UI", 8)
        tk.Label(panel_tot, text=texto, font=f, bg=BG)\
            .grid(row=2, column=col_idx, padx=2, pady=(2, 1))
        tk.Entry(panel_tot, textvariable=var, font=("Segoe UI", 9),
                 width=12, state="readonly", justify="right")\
            .grid(row=3, column=col_idx, padx=2, pady=(0, 2), sticky="ew")

    # ======= lógica totales =======
    items = []
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

    # ======= modal ítem =======
    def abrir_modal_item(edit=False):
        win = tk.Toplevel(root)
        win.title("Editar ítem" if edit else "Adicionar ítem")
        win.transient(root); win.grab_set(); win.configure(bg=BG)
        win.geometry("560x520")
        pad = dict(padx=6, pady=3)

        # --- Tipo bien/servicio ---
        tipo_var = tk.StringVar(value="Bien")
        tk.Radiobutton(win, text="Bien", variable=tipo_var, value="Bien", bg=BG)\
            .grid(row=0, column=0, sticky="w", **pad)
        tk.Radiobutton(win, text="Servicio", variable=tipo_var, value="Servicio", bg=BG)\
            .grid(row=0, column=1, sticky="w", **pad)

        # --- Buscar producto del inventario ---
        tk.Label(win, text="Buscar Producto", bg=BG, font=("Segoe UI", 9, "italic"))\
            .grid(row=1, column=0, sticky="e", **pad)
        e_buscar_prod = tk.Entry(win, width=30)
        e_buscar_prod.grid(row=1, column=1, sticky="w", **pad)

        prod_list = tk.Listbox(win, height=4, width=44, font=("Segoe UI", 9))
        prod_list.grid(row=2, column=1, sticky="w", padx=6, pady=2)

        def filtrar_productos(*_):
            prod_list.delete(0, tk.END)
            filtro = e_buscar_prod.get().strip()
            for p in prod_svc.listar(filtro)[:15]:
                # p = (codigo, nombre, precio, cantidad, descripcion)
                prod_list.insert(tk.END, f"{p[0] or '-'} | {p[1]} | S/.{p[2]:.2f} | Stock:{p[3]}")

        e_buscar_prod.bind("<KeyRelease>", filtrar_productos)

        def seleccionar_producto(_e=None):
            sel = prod_list.curselection()
            if not sel:
                return
            texto = prod_list.get(sel[0])
            partes = [x.strip() for x in texto.split("|")]
            codigo = partes[0] if partes[0] != "-" else ""
            nombre = partes[1]
            precio = partes[2].replace("S/.", "")
            e_cod.delete(0, tk.END); e_cod.insert(0, codigo)
            txt_desc.delete("1.0", tk.END); txt_desc.insert("1.0", nombre)
            e_val.delete(0, tk.END); e_val.insert(0, precio)
            recalcular_item()

        prod_list.bind("<Double-1>", seleccionar_producto)
        tk.Button(win, text="Seleccionar", font=("Segoe UI", 8),
                  command=seleccionar_producto)\
            .grid(row=2, column=0, sticky="e", padx=6)

        # --- Campos del ítem ---
        tk.Label(win, text="Cantidad", bg=BG).grid(row=3, column=0, sticky="e", **pad)
        e_cant = tk.Entry(win, width=14); e_cant.insert(0, "1")
        e_cant.grid(row=3, column=1, sticky="w", **pad)

        tk.Label(win, text="Unidad de Medida", bg=BG).grid(row=4, column=0, sticky="e", **pad)
        cb_un = ttk.Combobox(win, values=UNIDADES, state="readonly", width=20)
        cb_un.set("UNIDAD"); cb_un.grid(row=4, column=1, sticky="w", **pad)

        tk.Label(win, text="Código", bg=BG).grid(row=5, column=0, sticky="e", **pad)
        e_cod = tk.Entry(win, width=30); e_cod.grid(row=5, column=1, sticky="w", **pad)

        tk.Label(win, text="Descripción", bg=BG).grid(row=6, column=0, sticky="ne", **pad)
        txt_desc = tk.Text(win, width=46, height=3); txt_desc.grid(row=6, column=1, sticky="w", **pad)

        tk.Label(win, text="Imp. Bolsas Plásticas", bg=BG).grid(row=7, column=0, sticky="e", **pad)
        icb_si_no = tk.StringVar(value="NO")
        f_icb = tk.Frame(win, bg=BG)
        f_icb.grid(row=7, column=1, sticky="w", **pad)
        tk.Radiobutton(f_icb, text="SI", variable=icb_si_no, value="SI", bg=BG).pack(side="left")
        tk.Radiobutton(f_icb, text="NO", variable=icb_si_no, value="NO", bg=BG).pack(side="left", padx=12)

        tk.Label(win, text="Valor Unitario", bg=BG).grid(row=8, column=0, sticky="e", **pad)
        e_val = tk.Entry(win, width=18); e_val.insert(0, "0.00")
        e_val.grid(row=8, column=1, sticky="w", **pad)

        tk.Label(win, text="Descuento", bg=BG).grid(row=9, column=0, sticky="e", **pad)
        e_desc = tk.Entry(win, width=18); e_desc.insert(0, "0.00")
        e_desc.grid(row=9, column=1, sticky="w", **pad)

        tk.Label(win, text="ISC", bg=BG).grid(row=10, column=0, sticky="e", **pad)
        e_isc = tk.Entry(win, width=18); e_isc.insert(0, "0.00")
        e_isc.grid(row=10, column=1, sticky="w", **pad)

        # IGV - usar tasa de la configuración
        igv_pct_cfg = float(cfg_svc.obtener("igv_porcentaje") or "18")
        igv_default = igv_pct_cfg / 100.0
        tk.Label(win, text="IGV", bg=BG).grid(row=11, column=0, sticky="e", **pad)
        igv_rate = tk.DoubleVar(value=igv_default)
        f_igv = tk.Frame(win, bg=BG)
        f_igv.grid(row=11, column=1, sticky="w", **pad)
        tk.Radiobutton(f_igv, text=f"{igv_pct_cfg:g} %", variable=igv_rate, value=igv_default, bg=BG).pack(side="left")
        tk.Radiobutton(f_igv, text="10 %", variable=igv_rate, value=0.10, bg=BG).pack(side="left", padx=12)

        afect_var = tk.StringVar(value="Gravado")
        tk.Label(win, text="Afectación", bg=BG).grid(row=12, column=0, sticky="e", **pad)
        f_afect = tk.Frame(win, bg=BG)
        f_afect.grid(row=12, column=1, sticky="w", **pad)
        for af in AFECTACIONES:
            tk.Radiobutton(f_afect, text=af, variable=afect_var, value=af, bg=BG).pack(side="left", padx=4)

        tk.Label(win, text="Impuesto ICBPER", bg=BG).grid(row=13, column=0, sticky="e", **pad)
        e_icbper = tk.Entry(win, width=18, state="readonly")
        e_icbper.grid(row=13, column=1, sticky="w", **pad)

        tk.Label(win, text="Importe Total del Ítem", bg=BG).grid(row=14, column=0, sticky="e", **pad)
        e_total_item = tk.Entry(win, width=18, state="readonly")
        e_total_item.grid(row=14, column=1, sticky="w", **pad)

        icbper_tarifa_cfg = float(cfg_svc.obtener("icbper_tarifa") or "0.50")
        def icbper_tarifa():
            try: cant = float(e_cant.get() or "0")
            except ValueError: cant = 0
            return round(icbper_tarifa_cfg * cant, 2) if icb_si_no.get() == "SI" else 0.0

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
            for entry, val in ((e_icbper, icb), (e_total_item, total_item)):
                entry.config(state="normal"); entry.delete(0,"end"); entry.insert(0,f"{val:.2f}"); entry.config(state="readonly")

        for w in (e_cant, e_val, e_desc, e_isc): w.bind("<KeyRelease>", recalcular_item)
        afect_var.trace_add("write", lambda *_: recalcular_item())
        icb_si_no.trace_add("write", lambda *_: recalcular_item())
        igv_rate.trace_add("write", lambda *_: recalcular_item())

        idx_edit = None
        if edit:
            sel = tree.selection()
            if not sel: messagebox.showinfo("Editar","Selecciona un ítem."); win.destroy(); return
            idx_edit = tree.index(sel[0]); it = items[idx_edit]
            tipo_var.set(it.get("tipo","Bien"))
            e_cant.delete(0,"end"); e_cant.insert(0, str(it["cantidad"]))
            cb_un.set(it["unidad"]); e_cod.insert(0, it["codigo"])
            txt_desc.insert("1.0", it["descripcion"])
            icb_si_no.set("SI" if it["icbper"] > 0 else "NO")
            e_val.delete(0,"end"); e_val.insert(0, f"{it['valor_unit']:.2f}")
            e_desc.delete(0,"end"); e_desc.insert(0, f"{it.get('descuento',0.0):.2f}")
            e_isc.delete(0,"end"); e_isc.insert(0, f"{it.get('isc',0.0):.2f}")
            igv_rate.set(it.get("igv_rate",0.18)); afect_var.set(it["afectacion"])
            recalcular_item()

        def aceptar():
            try:
                cant = float(e_cant.get() or "0")
                vu   = float(e_val.get() or "0")
                desc = float(e_desc.get() or "0")
                isc  = float(e_isc.get() or "0")
            except ValueError:
                messagebox.showerror("Dato inválido", "Revisa cantidades y montos."); return

            bien  = tipo_var.get()
            unidad= cb_un.get()
            codigo= e_cod.get().strip()
            desc_txt = txt_desc.get("1.0", "end").strip()
            afect = afect_var.get()
            base = max(cant * vu - desc, 0)
            icb  = icbper_tarifa()
            igv_m= round(base * igv_rate.get(), 2) if afect == "Gravado" else 0.0
            total_i = base + igv_m + isc + icb
            if not desc_txt:
                messagebox.showwarning("Faltan datos", "Ingresa la descripción."); return

            data = dict(tipo=bien, unidad=unidad, codigo=codigo, descripcion=desc_txt,
                        afectacion=afect, cantidad=cant, valor_unit=vu,
                        descuento=desc, subtotal=base, igv=igv_m, igv_rate=igv_rate.get(),
                        isc=isc, icbper=icb, total=total_i)

            vals_row = (bien, afect, unidad, f"{cant:g}", codigo, desc_txt,
                        f"{vu:.2f}", f"{base:.2f}", f"{igv_m:.2f}", f"{isc:.2f}", f"{icb:.2f}", f"{total_i:.2f}")

            if edit and idx_edit is not None:
                items[idx_edit] = data
                iid = tree.get_children()[idx_edit]
                tree.item(iid, values=vals_row)
            else:
                items.append(data)
                tree.insert("", "end", values=vals_row)

            win.destroy(); recalcular_totales()

        btn_frame = tk.Frame(win, bg=BG)
        btn_frame.grid(row=15, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="✔ Aceptar", width=12, command=aceptar).pack(side="left", padx=8)
        tk.Button(btn_frame, text="✖ Cancelar", width=12, command=win.destroy).pack(side="left", padx=8)

        recalcular_item(); win.wait_window()

    def eliminar_sel():
        sel = tree.selection()
        if not sel: return
        if not messagebox.askyesno("Eliminar", "¿Eliminar el ítem seleccionado?"): return
        idx = tree.index(sel[0]); tree.delete(sel[0])
        try: items.pop(idx)
        except Exception: pass
        recalcular_totales()

    btn_add.config(command=lambda: abrir_modal_item(False))
    btn_edit.config(command=lambda: abrir_modal_item(True))
    btn_del.config(command=eliminar_sel)

    # ======= GUARDAR FACTURA =======
    def guardar_factura():
        if not cliente_actual[0]:
            messagebox.showwarning("Cliente", "Primero busca/registra un cliente."); return
        if not items:
            messagebox.showwarning("Ítems", "Agrega al menos un ítem a la factura."); return
        fecha = ent_fecha.get().strip()
        if not fecha:
            messagebox.showwarning("Fecha", "Ingresa la fecha de emisión."); return
        serie = cfg_svc.obtener("serie_factura") or "F001"
        try:
            _fac_id, num_fac = fac_svc.crear(
                cliente_id=cliente_actual[0],
                moneda=cb_moneda.get(),
                fecha_emision=fecha,
                subtotal=float(subtotal_var.get()),
                descuentos=float(descuentos_var.get()),
                valor_venta=float(valor_venta_var.get()),
                igv=float(igv_var.get()),
                isc=float(isc_var.get()),
                icbper=float(icbper_var.get()),
                otros_cargos=float(otros_cargos_var.get()),
                total=float(total_var.get()),
                items=items,
                serie=serie,
            )
            messagebox.showinfo("Factura Guardada",
                                f"Factura {num_fac} registrada exitosamente.\n"
                                f"Total: S/. {total_var.get()}")
            volver_cb()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la factura:\n{e}")

    # ======= BOTONERA =======
    pie = tk.Frame(frame_contenedor, bg=BG)
    pie.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 8))
    tk.Button(pie, text="Volver", font=("Segoe UI", 10, "bold"),
              command=volver_cb, bg="#007acc", fg="white", relief="flat",
              padx=12, pady=2)\
        .pack(side="left", padx=6)
    tk.Button(pie, text="Guardar Factura", font=("Segoe UI", 10, "bold"),
              bg="#28a745", fg="white", relief="flat", padx=12, pady=2,
              command=guardar_factura)\
        .pack(side="left", padx=6)
    tk.Button(pie, text="Cancelar", font=FUENTE, command=volver_cb)\
        .pack(side="left", padx=6)
