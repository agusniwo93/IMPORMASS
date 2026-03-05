# src/impormass/ui/login.py
import tkinter as tk
from tkinter import ttk, messagebox
from ..services import auth_service as auth
from .main_window import MainApp

BG = "#f0f4f8"


def _ventana_registro(root):
    win = tk.Toplevel(root)
    win.title("Registro de Usuario")
    win.geometry("400x280")
    win.minsize(360, 260)
    win.configure(bg=BG)
    win.transient(root)
    win.grab_set()

    for i in range(5):
        win.rowconfigure(i, weight=0)
    win.rowconfigure(5, weight=1)
    win.columnconfigure(1, weight=1)

    tk.Label(win, text="REGISTRO", font=("Segoe UI", 14, "bold"), bg=BG)\
        .grid(row=0, column=0, columnspan=2, pady=(12, 8))

    tk.Label(win, text="Usuario:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=1, column=0, padx=(12, 6), pady=6, sticky="e")
    e_u = tk.Entry(win, font=("Segoe UI", 11), width=24)
    e_u.grid(row=1, column=1, padx=(0, 12), pady=6, sticky="ew")

    tk.Label(win, text="Contraseña:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=2, column=0, padx=(12, 6), pady=6, sticky="e")
    e_p = tk.Entry(win, show="*", font=("Segoe UI", 11))
    e_p.grid(row=2, column=1, padx=(0, 12), pady=6, sticky="ew")

    tk.Label(win, text="Rol:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=3, column=0, padx=(12, 6), pady=6, sticky="e")
    cb_rol = ttk.Combobox(win, values=["vendedor", "almacenero"],
                           state="readonly", font=("Segoe UI", 11), width=20)
    cb_rol.set("vendedor")
    cb_rol.grid(row=3, column=1, padx=(0, 12), pady=6, sticky="w")

    def registrar():
        u = e_u.get().strip()
        p = e_p.get().strip()
        rol = cb_rol.get()
        if not u or not p:
            messagebox.showwarning("Campos vacíos", "Ingresa usuario y contraseña.")
            return
        if len(p) < 4:
            messagebox.showwarning("Contraseña corta",
                                   "La contraseña debe tener al menos 4 caracteres.")
            return
        if auth.registrar(u, p, rol):
            messagebox.showinfo("OK", f"Usuario '{u}' creado con rol '{rol}'.")
            win.destroy()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")

    tk.Button(win, text="Registrar", font=("Segoe UI", 11), command=registrar,
              bg="#007acc", fg="white", relief="flat", padx=12)\
        .grid(row=4, column=1, padx=12, pady=12, sticky="e")

    e_u.focus_set()


def run_login():
    root = tk.Tk()
    root.title("IMPORMASS - Inicio de Sesión")
    root.geometry("420x260")
    root.minsize(380, 240)
    root.configure(bg=BG)

    for i in range(5):
        root.rowconfigure(i, weight=0)
    root.rowconfigure(5, weight=1)
    root.columnconfigure(1, weight=1)

    tk.Label(root, text="IMPORMASS", font=("Segoe UI", 18, "bold"),
             bg=BG, fg="#007acc")\
        .grid(row=0, column=0, columnspan=2, pady=(16, 4))
    tk.Label(root, text="Sistema de Ventas y Almacén",
             font=("Segoe UI", 9), bg=BG, fg="#555")\
        .grid(row=1, column=0, columnspan=2, pady=(0, 12))

    tk.Label(root, text="Usuario:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=2, column=0, padx=(16, 6), pady=6, sticky="e")
    e_u = tk.Entry(root, font=("Segoe UI", 11))
    e_u.grid(row=2, column=1, padx=(0, 16), pady=6, sticky="ew")

    tk.Label(root, text="Contraseña:", bg=BG, font=("Segoe UI", 10))\
        .grid(row=3, column=0, padx=(16, 6), pady=6, sticky="e")
    e_p = tk.Entry(root, show="*", font=("Segoe UI", 11))
    e_p.grid(row=3, column=1, padx=(0, 16), pady=6, sticky="ew")

    def entrar(_event=None):
        u = e_u.get().strip()
        p = e_p.get().strip()
        if not u or not p:
            messagebox.showwarning("Campos vacíos", "Ingresa usuario y contraseña.")
            return
        ok, rol = auth.validar(u, p)
        if ok:
            root.destroy()
            MainApp(usuario=u, rol=rol).mainloop()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=12)

    tk.Button(btn_frame, text="Registrarse", font=("Segoe UI", 10),
              command=lambda: _ventana_registro(root))\
        .pack(side="left", padx=10)

    tk.Button(btn_frame, text="Iniciar Sesión", font=("Segoe UI", 11, "bold"),
              bg="#007acc", fg="white", relief="flat", padx=14,
              command=entrar)\
        .pack(side="left", padx=10)

    # Enter para iniciar sesión
    root.bind("<Return>", entrar)
    e_u.focus_set()
    root.mainloop()
