# src/impormass/ui/login.py
import tkinter as tk
from tkinter import messagebox
from ..services import auth_service as auth
from .main_window import MainApp

def _ventana_registro(root):
    win = tk.Toplevel(root); win.title("Registro")
    win.geometry("360x200"); win.minsize(320, 180)
    win.rowconfigure(3, weight=1); win.columnconfigure(1, weight=1)

    tk.Label(win, text="Usuario").grid(row=0, column=0, padx=8, pady=(12,6), sticky="e")
    e_u = tk.Entry(win, width=28); e_u.grid(row=0, column=1, padx=8, pady=(12,6), sticky="ew")

    tk.Label(win, text="Contraseña").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    e_p = tk.Entry(win, show="*"); e_p.grid(row=1, column=1, padx=8, pady=6, sticky="ew")

    def registrar():
        if auth.registrar(e_u.get(), e_p.get()):
            messagebox.showinfo("OK", "Usuario creado"); win.destroy()
        else:
            messagebox.showerror("Error", "Usuario ya existe")

    tk.Button(win, text="Registrar", command=registrar)\
        .grid(row=2, column=1, padx=8, pady=12, sticky="e")

def run_login():
    root = tk.Tk(); root.title("Inicio de Sesión")
    root.geometry("380x220"); root.minsize(340, 200)
    root.rowconfigure(3, weight=1); root.columnconfigure(1, weight=1)

    tk.Label(root, text="Usuario").grid(row=0, column=0, padx=10, pady=(16,8), sticky="e")
    e_u = tk.Entry(root); e_u.grid(row=0, column=1, padx=10, pady=(16,8), sticky="ew")

    tk.Label(root, text="Contraseña").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    e_p = tk.Entry(root, show="*"); e_p.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

    def entrar():
        if auth.validar(e_u.get(), e_p.get()):
            root.destroy()
            MainApp().mainloop()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    tk.Button(root, text="Iniciar Sesión", command=entrar)\
        .grid(row=2, column=1, padx=10, pady=10, sticky="e")
    tk.Button(root, text="Registrarse", command=lambda: _ventana_registro(root))\
        .grid(row=2, column=0, padx=10, pady=10, sticky="w")

    root.mainloop()
