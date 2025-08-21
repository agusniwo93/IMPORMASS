import tkinter as tk
from productos_consulta import ventana_productos_consulta

def usar_productos_registro(frame, volver_funcion):
    from productos_ui import ventana_productos_registro
    ventana_productos_registro(frame, volver_funcion)

# Esta función recibe también 'volver_funcion'
def menu_productos(frame, volver_funcion):
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame.pack_propagate(False)

    tk.Label(frame, text="GESTIÓN DE PRODUCTOS", font=("Segoe UI", 18, "bold"), bg="#f8f8f8").pack(pady=20)

    botones_info = [
        ("📥 Registrar Producto", lambda: usar_productos_registro(frame, volver_funcion)),
        ("🔍 Consultar Productos", lambda: ventana_productos_consulta(frame)),
        ("⬅ Volver al Menú Principal", volver_funcion)
    ]

    for texto, accion in botones_info:
        tk.Button(frame, text=texto, font=("Segoe UI", 13), width=35, height=2,
                  bg="#007acc", fg="white", activebackground="#005f99",
                  relief="flat", command=accion).pack(pady=12)
def menu_productos(frame, volver_funcion):
    for widget in frame.winfo_children():
        widget.destroy()

    frame.pack_propagate(False)

    tk.Label(frame, text="GESTIÓN DE PRODUCTOS", font=("Segoe UI", 18, "bold"), bg="#f8f8f8").pack(pady=20)

    botones_info = [
        ("📅 Registrar Producto", lambda: usar_productos_registro(frame, lambda: menu_productos(frame, volver_funcion))),
        ("🔍 Consultar Productos", lambda: ventana_productos_consulta(frame, volver_funcion)),
        ("⬅ Volver al Menú Principal", volver_funcion)
    ]

    for texto, accion in botones_info:
        tk.Button(frame, text=texto, font=("Segoe UI", 13), width=35, height=2,
                bg="#007acc", fg="white", activebackground="#005f99",
                relief="flat", command=accion).pack(pady=12)