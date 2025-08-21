import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from productos_menu import menu_productos

def ventana_productos_registro(frame, volver_funcion):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_propagate(False)

    tk.Label(frame, text="REGISTRO DE PRODUCTOS", font=("Segoe UI", 20, "bold"), bg="#f8f8f8").pack(pady=20)

    entrada_nombre = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_codigo = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_precio = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_cantidad = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_descripcion = tk.Text(frame, width=60, height=6, font=("Segoe UI", 12))

    campos = [
        ("Nombre del producto", entrada_nombre),
        ("Código (opcional)", entrada_codigo),
        ("Precio (S/.)", entrada_precio),
        ("Cantidad", entrada_cantidad),
        ("Descripción", entrada_descripcion)
    ]

    for label, entrada in campos:
        tk.Label(frame, text=label, bg="#f8f8f8", font=("Segoe UI", 11)).pack(pady=(5, 0))
        entrada.pack(pady=(0, 5))

    tk.Label(frame, text="🔍 Buscar producto por nombre:", bg="#f8f8f8", font=("Segoe UI", 11)).pack(pady=(10, 0))
    entrada_busqueda = tk.Entry(frame, width=60, font=("Segoe UI", 12))
    entrada_busqueda.pack(pady=(0, 10))

    contenedor_tabla = tk.Frame(frame)
    contenedor_tabla.pack(fill="both", expand=True)

    scroll_y = tk.Scrollbar(contenedor_tabla, orient="vertical")
    scroll_x = tk.Scrollbar(contenedor_tabla, orient="horizontal")

    tree = ttk.Treeview(contenedor_tabla, columns=("Código", "Nombre", "Precio", "Cantidad", "Descripción"),
                        show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    scroll_y.config(command=tree.yview)
    scroll_y.pack(side="right", fill="y")

    scroll_x.config(command=tree.xview)
    scroll_x.pack(side="bottom", fill="x")

    tree.pack(fill="both", expand=True)

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

    entrada_busqueda.bind("<KeyRelease>", lambda e: cargar_productos(entrada_busqueda.get()))

    def guardar_producto():
        nombre = entrada_nombre.get().strip()
        codigo = entrada_codigo.get().strip()
        precio = entrada_precio.get().strip()
        cantidad = entrada_cantidad.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()

        if not (nombre and codigo and precio and cantidad):
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
            return

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showwarning("Valor inválido", "Precio y cantidad deben ser números.")
            return

        conexion = sqlite3.connect("facturador.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM productos WHERE codigo = ?", (codigo,))
        if cursor.fetchone():
            messagebox.showerror("Código duplicado", "Ya existe un producto con ese código.")
            conexion.close()
            return

        cursor.execute("INSERT INTO productos (nombre, codigo, precio, cantidad, descripcion) VALUES (?, ?, ?, ?, ?)",
                    (nombre, codigo, precio, cantidad, descripcion))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Producto guardado correctamente.")
        cancelar_edicion()
        cargar_productos()

    def eliminar_producto():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un producto para eliminar.")
            return
        codigo = tree.item(seleccionado, "values")[0]
        if messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el producto con código {codigo}?"):
            conexion = sqlite3.connect("facturador.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
            conexion.commit()
            conexion.close()
            cargar_productos()
            messagebox.showinfo("Eliminado", "Producto eliminado correctamente.")

    def cargar_para_editar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un producto para editar.")
            return
        valores = tree.item(seleccionado, "values")
        entrada_codigo.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)
        entrada_cantidad.delete(0, tk.END)
        entrada_descripcion.delete("1.0", tk.END)

        entrada_codigo.insert(0, valores[0])
        entrada_nombre.insert(0, valores[1])
        entrada_precio.insert(0, valores[2])
        entrada_cantidad.insert(0, valores[3])
        entrada_descripcion.insert("1.0", valores[4])

    def actualizar_producto():
        codigo = entrada_codigo.get().strip()
        nombre = entrada_nombre.get().strip()
        precio = entrada_precio.get().strip()
        cantidad = entrada_cantidad.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()

        if not (nombre and codigo and precio and cantidad):
            messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
            return

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showwarning("Valor inválido", "Precio y cantidad deben ser números.")
            return

        conexion = sqlite3.connect("facturador.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=?, precio=?, cantidad=?, descripcion=? WHERE codigo=?",
                    (nombre, precio, cantidad, descripcion, codigo))
        conexion.commit()
        conexion.close()

        cargar_productos()
        messagebox.showinfo("Actualizado", "Producto actualizado correctamente.")
        cancelar_edicion()

    def cancelar_edicion():
        entrada_codigo.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)
        entrada_cantidad.delete(0, tk.END)
        entrada_descripcion.delete("1.0", tk.END)

    acciones = tk.Frame(frame, bg="#f8f8f8")
    acciones.pack(pady=10)

    fila1 = tk.Frame(acciones, bg="#f8f8f8")
    fila1.pack(pady=5)
    fila2 = tk.Frame(acciones, bg="#f8f8f8")
    fila2.pack(pady=5)

    tk.Button(fila1, text="✏ Editar seleccionado", command=cargar_para_editar, width=20, height=2,
            font=("Segoe UI", 10)).pack(side="left", padx=5)
    tk.Button(fila1, text="✅ Actualizar", command=actualizar_producto, width=20, height=2,
            font=("Segoe UI", 10)).pack(side="left", padx=5)
    tk.Button(fila1, text="🛑 Cancelar edición", command=cancelar_edicion, width=20, height=2,
            font=("Segoe UI", 10)).pack(side="left", padx=5)

    tk.Button(fila2, text="❌ Eliminar", command=eliminar_producto, width=20, height=2,
            font=("Segoe UI", 10)).pack(side="left", padx=5)
    tk.Button(fila2, text="💾 Guardar Producto", command=guardar_producto, bg="#007acc", fg="white",
            width=20, height=2, font=("Segoe UI", 10)).pack(side="left", padx=5)

    botones_frame = tk.Frame(frame, bg="#f8f8f8")
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="⬅ Volver", command=volver_funcion,
            font=("Segoe UI", 10), width=20).pack(side="left", padx=5)

    cargar_productos()