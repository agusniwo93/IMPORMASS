import tkinter as tk
from tkinter import ttk
import sqlite3

def ventana_productos_consulta(frame, volver_funcion):
    from productos_menu import menu_productos  # Evita ciclo de importación

    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_propagate(False)

    tk.Label(frame, text="CONSULTA DE PRODUCTOS", font=("Segoe UI", 20, "bold"), bg="#f8f8f8").pack(pady=20)
    tk.Label(frame, text="Buscar producto por nombre:", bg="#f8f8f8", font=("Segoe UI", 11)).pack(pady=10)

    entrada_busqueda = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_busqueda.pack()

    tree = ttk.Treeview(frame, columns=("Código", "Nombre", "Precio", "Cantidad", "Descripción"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(pady=20, fill="both", expand=True)

    # ✅ Esta función estaba mal indentada antes
    def cargar_productos(filtro=""):
        for item in tree.get_children():
            tree.delete(item)
        conexion = sqlite3.connect("facturador.db")
        cursor = conexion.cursor()
        if filtro:
            cursor.execute("""
                SELECT codigo, nombre, precio, cantidad, descripcion
                FROM productos
                WHERE nombre LIKE ?
            """, ('%' + filtro + '%',))
        else:
            cursor.execute("SELECT codigo, nombre, precio, cantidad, descripcion FROM productos")
        for fila in cursor.fetchall():
            tree.insert("", tk.END, values=fila)
        conexion.close()

    # 🔍 Búsqueda reactiva
    entrada_busqueda.bind("<KeyRelease>", lambda e: cargar_productos(entrada_busqueda.get()))
    
    # 📦 Carga inicial
    cargar_productos()

    # ⬅ Botón volver
    tk.Button(frame, text="⬅ Volver", command=lambda: menu_productos(frame, volver_funcion),
            bg="#cccccc", font=("Segoe UI", 11)).pack(pady=(10,20))