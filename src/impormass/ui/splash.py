# src/impormass/ui/splash.py
import tkinter as tk
from PIL import Image, ImageTk
from ..config import ASSETS

def run_splash(next_fn, duration_ms: int = 4000):
    """
    Muestra un splash y, al terminar, ejecuta next_fn().
    next_fn debe crear su propia ventana (p.ej., run_login() o MainApp()).
    """
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg="#ffffff")
    # posición: centrado aproximado
    root.geometry("600x400+400+150")

    # ---------- CARGAR FRAMES DEL GIF ----------
    frames = []
    try:
        gif_path = ASSETS / "tigrecarga.gif"   # pon tu gif en assets/
        gif = Image.open(gif_path)
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass
    except Exception as e:
        print("Error al cargar el GIF:", e)
        frames = []

    # ---------- WIDGETS ----------
    label_gif = tk.Label(root, bg="#ffffff")
    label_gif.pack(pady=40)

    bar_frame = tk.Frame(root, bg="#dddddd", width=400, height=15)
    bar_frame.pack(pady=10)
    progress = tk.Frame(bar_frame, bg="#007acc", width=10, height=15)
    progress.place(x=0, y=0)

    # ---------- ANIMACIÓN ----------
    def animar(i=0, w=10):
        if frames:
            label_gif.configure(image=frames[i])
            root.after(100, animar, (i + 1) % len(frames), w)

        if w <= 400:
            progress.place(width=w)
            root.after(30, animar, i, w + 10)

    def continuar():
        try:
            root.destroy()   # cierra splash
        finally:
            next_fn()        # lanza la siguiente pantalla

    root.after(100, animar)
    root.after(duration_ms, continuar)
    root.mainloop()
