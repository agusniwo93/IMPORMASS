# src/impormass/ui/configuracion.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ..services import config_service as cfg
from datetime import datetime

BG = "#f8f8f8"


def vista_configuracion(frame, volver_funcion):
    for w in frame.winfo_children():
        w.destroy()

    for i in range(3):
        frame.rowconfigure(i, weight=0)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)

    tk.Label(frame, text="CONFIGURACION DEL SISTEMA",
             font=("Segoe UI", 20, "bold"), bg=BG)\
        .grid(row=0, column=0, pady=(10, 6), sticky="n")

    # --- Notebook con pestañas ---
    nb = ttk.Notebook(frame)
    nb.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 6))

    # Cargar todos los valores actuales
    config = cfg.obtener_todo()

    # ========================================================
    # TAB 1: Datos de la Empresa
    # ========================================================
    tab_empresa = tk.Frame(nb, bg=BG, padx=16, pady=12)
    nb.add(tab_empresa, text="  Datos de la Empresa  ")

    tab_empresa.columnconfigure(1, weight=1)

    campos_empresa = [
        ("RUC del Emisor:", "empresa_ruc", 14),
        ("Razon Social:", "empresa_razon_social", 40),
        ("Nombre Comercial:", "empresa_nombre_comercial", 40),
        ("Direccion Fiscal:", "empresa_direccion", 50),
        ("Departamento:", "empresa_departamento", 20),
        ("Provincia:", "empresa_provincia", 20),
        ("Distrito:", "empresa_distrito", 20),
        ("Ubigeo:", "empresa_ubigeo", 8),
        ("Telefono:", "empresa_telefono", 16),
        ("Email:", "empresa_email", 30),
    ]

    entries_empresa = {}
    for i, (label, key, width) in enumerate(campos_empresa):
        tk.Label(tab_empresa, text=label, bg=BG, font=("Segoe UI", 10),
                 anchor="e", width=18)\
            .grid(row=i, column=0, sticky="e", padx=(0, 8), pady=4)
        e = tk.Entry(tab_empresa, font=("Segoe UI", 11), width=width)
        e.grid(row=i, column=1, sticky="ew", pady=4)
        e.insert(0, config.get(key, ""))
        entries_empresa[key] = e

    def guardar_empresa():
        datos = {}
        for key, entry in entries_empresa.items():
            datos[key] = entry.get().strip()
        cfg.guardar_todo(datos)
        messagebox.showinfo("OK", "Datos de la empresa guardados correctamente.")

    btn_emp = tk.Frame(tab_empresa, bg=BG)
    btn_emp.grid(row=len(campos_empresa), column=0, columnspan=2, pady=(12, 4))
    tk.Button(btn_emp, text="Guardar Datos Empresa", font=("Segoe UI", 11, "bold"),
              bg="#28a745", fg="white", relief="flat", padx=16, pady=4,
              command=guardar_empresa)\
        .pack()

    # ========================================================
    # TAB 2: Facturación
    # ========================================================
    tab_fact = tk.Frame(nb, bg=BG, padx=16, pady=12)
    nb.add(tab_fact, text="  Facturacion  ")

    tab_fact.columnconfigure(1, weight=1)

    # Serie de Factura
    tk.Label(tab_fact, text="Serie de Factura:", bg=BG, font=("Segoe UI", 10),
             anchor="e", width=18)\
        .grid(row=0, column=0, sticky="e", padx=(0, 8), pady=6)
    e_serie_fac = tk.Entry(tab_fact, font=("Segoe UI", 11), width=10)
    e_serie_fac.grid(row=0, column=1, sticky="w", pady=6)
    e_serie_fac.insert(0, config.get("serie_factura", "F001"))

    # Serie de Boleta
    tk.Label(tab_fact, text="Serie de Boleta:", bg=BG, font=("Segoe UI", 10),
             anchor="e", width=18)\
        .grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
    e_serie_bol = tk.Entry(tab_fact, font=("Segoe UI", 11), width=10)
    e_serie_bol.grid(row=1, column=1, sticky="w", pady=6)
    e_serie_bol.insert(0, config.get("serie_boleta", "B001"))

    # IGV
    tk.Label(tab_fact, text="IGV (%):", bg=BG, font=("Segoe UI", 10),
             anchor="e", width=18)\
        .grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
    e_igv = tk.Entry(tab_fact, font=("Segoe UI", 11), width=8)
    e_igv.grid(row=2, column=1, sticky="w", pady=6)
    e_igv.insert(0, config.get("igv_porcentaje", "18"))

    # ICBPER tarifa
    tk.Label(tab_fact, text="ICBPER tarifa (S/.):", bg=BG, font=("Segoe UI", 10),
             anchor="e", width=18)\
        .grid(row=3, column=0, sticky="e", padx=(0, 8), pady=6)
    e_icbper = tk.Entry(tab_fact, font=("Segoe UI", 11), width=8)
    e_icbper.grid(row=3, column=1, sticky="w", pady=6)
    e_icbper.insert(0, config.get("icbper_tarifa", "0.50"))

    # Moneda por defecto
    tk.Label(tab_fact, text="Moneda por Defecto:", bg=BG, font=("Segoe UI", 10),
             anchor="e", width=18)\
        .grid(row=4, column=0, sticky="e", padx=(0, 8), pady=6)
    cb_moneda = ttk.Combobox(tab_fact, values=["SOLES", "DOLARES"],
                              state="readonly", font=("Segoe UI", 11), width=14)
    cb_moneda.set(config.get("moneda_defecto", "SOLES"))
    cb_moneda.grid(row=4, column=1, sticky="w", pady=6)

    # Explicación
    tk.Label(tab_fact, text="Nota: El IGV se aplica a items con afectacion 'Gravado'.\n"
             "La tarifa ICBPER se aplica por unidad de bolsa plastica.",
             bg=BG, font=("Segoe UI", 9, "italic"), fg="#666",
             justify="left")\
        .grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 4))

    def guardar_facturacion():
        try:
            igv_val = float(e_igv.get().strip())
            icb_val = float(e_icbper.get().strip())
            if igv_val < 0 or igv_val > 100:
                messagebox.showwarning("IGV", "El IGV debe estar entre 0 y 100%.")
                return
            if icb_val < 0:
                messagebox.showwarning("ICBPER", "La tarifa ICBPER no puede ser negativa.")
                return
        except ValueError:
            messagebox.showwarning("Valor", "IGV y ICBPER deben ser numeros validos.")
            return

        datos = {
            "serie_factura": e_serie_fac.get().strip().upper(),
            "serie_boleta": e_serie_bol.get().strip().upper(),
            "igv_porcentaje": e_igv.get().strip(),
            "icbper_tarifa": e_icbper.get().strip(),
            "moneda_defecto": cb_moneda.get(),
        }
        cfg.guardar_todo(datos)
        messagebox.showinfo("OK", "Configuracion de facturacion guardada.")

    btn_fact = tk.Frame(tab_fact, bg=BG)
    btn_fact.grid(row=6, column=0, columnspan=2, pady=(12, 4))
    tk.Button(btn_fact, text="Guardar Config. Facturacion", font=("Segoe UI", 11, "bold"),
              bg="#28a745", fg="white", relief="flat", padx=16, pady=4,
              command=guardar_facturacion)\
        .pack()

    # ========================================================
    # TAB 3: Base de Datos
    # ========================================================
    tab_db = tk.Frame(nb, bg=BG, padx=16, pady=12)
    nb.add(tab_db, text="  Base de Datos  ")

    tab_db.columnconfigure(1, weight=1)

    info = cfg.obtener_info_db()

    tk.Label(tab_db, text="Informacion de la Base de Datos",
             font=("Segoe UI", 13, "bold"), bg=BG)\
        .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

    info_campos = [
        ("Ruta:", info.get("ruta", "—")),
        ("Tamaño:", info.get("tamaño", "—")),
        ("Usuarios:", info.get("registros_usuarios", "0")),
        ("Productos:", info.get("registros_productos", "0")),
        ("Clientes:", info.get("registros_clientes", "0")),
        ("Facturas:", info.get("registros_facturas", "0")),
        ("Det. Facturas:", info.get("registros_factura_detalle", "0")),
    ]

    for i, (label, valor) in enumerate(info_campos):
        tk.Label(tab_db, text=label, bg=BG, font=("Segoe UI", 10, "bold"),
                 anchor="e", width=15)\
            .grid(row=i + 1, column=0, sticky="e", padx=(0, 8), pady=3)
        tk.Label(tab_db, text=valor, bg=BG, font=("Segoe UI", 10),
                 anchor="w")\
            .grid(row=i + 1, column=1, sticky="w", pady=3)

    def exportar_backup():
        ruta = filedialog.asksaveasfilename(
            title="Exportar Backup",
            defaultextension=".db",
            initialfile=f"impormass_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            filetypes=[("SQLite DB", "*.db"), ("Todos", "*.*")]
        )
        if ruta:
            if cfg.exportar_backup(ruta):
                messagebox.showinfo("OK", f"Backup exportado exitosamente a:\n{ruta}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el backup.")

    def actualizar_info():
        new_info = cfg.obtener_info_db()
        for i, (label, _) in enumerate(info_campos):
            key = label.rstrip(":").lower()
            # Buscar el valor en new_info
            if key == "ruta":
                val = new_info.get("ruta", "—")
            elif "tama" in key:
                val = new_info.get("tamaño", "—")
            else:
                # Mapear nombre a clave
                mapping = {
                    "usuarios": "registros_usuarios",
                    "productos": "registros_productos",
                    "clientes": "registros_clientes",
                    "facturas": "registros_facturas",
                    "det. facturas": "registros_factura_detalle",
                }
                clave = mapping.get(key, "")
                val = new_info.get(clave, "0")
            # Actualizar label (child at row i+1, col 1)
            for child in tab_db.grid_slaves(row=i + 1, column=1):
                child.config(text=val)

    btn_db = tk.Frame(tab_db, bg=BG)
    btn_db.grid(row=len(info_campos) + 2, column=0, columnspan=2, pady=(16, 4))
    tk.Button(btn_db, text="Exportar Backup", font=("Segoe UI", 11),
              bg="#007acc", fg="white", relief="flat", padx=14, pady=4,
              command=exportar_backup)\
        .pack(side="left", padx=8)
    tk.Button(btn_db, text="Actualizar Info", font=("Segoe UI", 11),
              command=actualizar_info)\
        .pack(side="left", padx=8)

    # --- Botón volver ---
    tk.Button(frame, text="Volver al Menu Principal", font=("Segoe UI", 11, "bold"),
              command=volver_funcion, bg="#007acc", fg="white",
              activebackground="#005f99", relief="flat", padx=16, pady=4)\
        .grid(row=2, column=0, pady=(4, 10))
