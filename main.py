import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from productos_ui import ventana_productos_registro
from productos_consulta import ventana_productos_consulta

# ------------------- VENTANA PRINCIPAL ------------------- #
ventana = tk.Tk()
ventana.title("Facturador Electrónico SUNAT")
ventana.state('zoomed')  # Pantalla completa
ventana.configure(bg="#f8f8f8")

# ------------------- CONTENEDOR CENTRAL ------------------- #
frame_contenido = tk.Frame(ventana, bg="#f8f8f8")
frame_contenido.pack(fill="both", expand=True)

contenido_interno = tk.Frame(frame_contenido, bg="#f8f8f8")
contenido_interno.place(relx=0.5, rely=0.48, anchor="center")

# ------------------- FUNCIONES ------------------- #
def crear_factura():
    from facturas_registro import ventana_facturas_registro
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    ventana_facturas_registro(frame_contenido, cargar_menu_principal)




def ver_facturas():
    messagebox.showinfo("Ver Facturas", "Aquí se mostrarán las facturas emitidas.")

def clientes():
    messagebox.showinfo("Clientes", "Aquí se gestionarán los clientes.")

def productos():
    from productos_menu import menu_productos
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    menu_productos(frame_contenido, cargar_menu_principal)

def configuracion():
    messagebox.showinfo("Configuración", "Aquí se configurará el sistema.")

def cargar_menu_principal():
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    contenido = tk.Frame(frame_contenido, bg="#f8f8f8")
    contenido.place(relx=0.5, rely=0.48, anchor="center")

    try:
        imagen_logo = Image.open("logo_impormass.png")
        ancho_max, alto_max = 700, 300
        ancho_original, alto_original = imagen_logo.size
        proporcion = min(ancho_max / ancho_original, alto_max / alto_original)
        nuevo_tamano = (int(ancho_original * proporcion), int(alto_original * proporcion))
        imagen_logo = imagen_logo.resize(nuevo_tamano, Image.LANCZOS)
        logo = ImageTk.PhotoImage(imagen_logo)
        logo_label = tk.Label(contenido, image=logo, bg="#f8f8f8")
        logo_label.image = logo
        logo_label.pack(pady=(20, 30))
    except:
        tk.Label(contenido, text="IMPORMASS", font=("Arial", 30, "bold"), bg="#f8f8f8", fg="#007acc").pack(pady=40)

    botones_info = [
        ("📟 Crear Factura", crear_factura),
        ("📂 Ver Facturas", ver_facturas),
        ("👥 Clientes", clientes),
        ("📦 Productos", productos),
        ("⚙ Configuración", configuracion)
    ]

    for texto, accion in botones_info:
        boton = tk.Button(contenido, text=texto, font=("Segoe UI", 14), width=38, height=2,
                        bg="#007acc", fg="white", activebackground="#005f99",
                        relief="flat", command=accion)
        boton.pack(pady=12)

# ------------------- INICIO ------------------- #
cargar_menu_principal()
ventana.mainloop()