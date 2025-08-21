import tkinter as tk
from tkinter import messagebox
import sqlite3
from registro import ventana_registro
import subprocess
import sys

def ventana_login():
    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    ventana.geometry("350x200")

    tk.Label(ventana, text="Usuario").pack(pady=5)
    entrada_usuario = tk.Entry(ventana, width=30)
    entrada_usuario.pack()

    tk.Label(ventana, text="Contraseña").pack(pady=5)
    entrada_clave = tk.Entry(ventana, show="*", width=30)
    entrada_clave.pack()

    def iniciar_sesion():
        usuario = entrada_usuario.get().strip()
        clave = entrada_clave.get().strip()

        conexion = sqlite3.connect("facturador.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            messagebox.showinfo("Éxito", "Inicio de sesión correcto.")
            ventana.destroy()
            # Ejecutar main.py (ventana principal)
            subprocess.Popen([sys.executable, "main.py"])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    # Botones
    tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    tk.Button(ventana, text="Registrarse", command=ventana_registro).pack()

    ventana.mainloop()


if __name__ == "__main__":
    ventana_login()
