import tkinter as tk
from tkinter import messagebox
import sqlite3

def ventana_registro():
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuario")
    ventana.geometry("350x250")

    tk.Label(ventana, text="Nuevo Usuario").pack(pady=10)
    entrada_usuario = tk.Entry(ventana, width=30)
    entrada_usuario.pack()

    tk.Label(ventana, text="Contraseña").pack(pady=10)
    entrada_clave = tk.Entry(ventana, show="*", width=30)
    entrada_clave.pack()

    tk.Label(ventana, text="Confirmar Contraseña").pack(pady=10)
    entrada_clave_confirmar = tk.Entry(ventana, show="*", width=30)
    entrada_clave_confirmar.pack()

    def registrar():
        usuario = entrada_usuario.get().strip()
        clave = entrada_clave.get().strip()
        confirmar = entrada_clave_confirmar.get().strip()

        if not usuario or not clave or not confirmar:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        if clave != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        try:
            conexion = sqlite3.connect("facturador.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (?, ?)", (usuario, clave))
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Registro exitoso", "Usuario creado correctamente.")
            ventana.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=20)
