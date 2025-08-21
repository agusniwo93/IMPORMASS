import tkinter as tk
from PIL import Image, ImageTk
import os

# ---------- MOSTRAR MENU PRINCIPAL DESPUÉS DE CARGAR ---------- #
def mostrar_menu_principal():
    splash.destroy()
    os.system("python main.py")  # Asegúrate que main.py sea tu menú principal

# ---------- CREAR VENTANA SPLASH ---------- #
splash = tk.Tk()
splash.overrideredirect(True)
splash.configure(bg="#ffffff")
splash.geometry("600x400+400+150")  # Puedes ajustar tamaño y posición

# ---------- CARGAR FRAMES DEL GIF ---------- #
try:
    gif = Image.open("tigrecarga.gif")
    frames = []
    while True:
        frames.append(ImageTk.PhotoImage(gif.copy()))
        gif.seek(len(frames))
except EOFError:
    pass
except Exception as e:
    print("Error al cargar el GIF:", e)
    frames = []

# ---------- MOSTRAR GIF EN LABEL ---------- #
label_gif = tk.Label(splash, bg="#ffffff")
label_gif.pack(pady=40)

# ---------- BARRA DE CARGA SIMBÓLICA ---------- #
bar_frame = tk.Frame(splash, bg="#dddddd", width=400, height=15)
bar_frame.pack(pady=10)
progress = tk.Frame(bar_frame, bg="#007acc", width=10, height=15)
progress.place(x=0, y=0)

# ---------- ANIMACIÓN ---------- #
def animar(i=0, w=10):
    if frames:
        label_gif.configure(image=frames[i])
        splash.after(100, animar, (i + 1) % len(frames), w)

    if w <= 400:
        progress.place(width=w)
        splash.after(30, animar, i, w + 10)

# ---------- INICIAR ANIMACIÓN Y CONTADOR ---------- #
splash.after(100, animar)
splash.after(4000, mostrar_menu_principal)  # 4 segundos de splash
splash.mainloop()
