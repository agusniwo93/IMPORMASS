# src/impormass/ui/splash.py
import tkinter as tk
from PIL import Image, ImageTk
from ..config import ASSETS


def run_splash(next_fn, duration_ms: int = 3000):
    """
    Muestra un splash centrado y, al terminar, ejecuta next_fn().
    next_fn debe crear su propia ventana (p.ej., run_login()).
    """
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg="#ffffff")

    w, h = 500, 350
    # Centrar en pantalla
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- LOGO / GIF ----------
    frames = []
    logo_img = None

    # Intentar cargar GIF animado
    try:
        gif_path = ASSETS / "tigrecarga.gif"
        gif = Image.open(gif_path)
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy().resize((200, 200), Image.LANCZOS)))
            gif.seek(len(frames))
    except EOFError:
        pass
    except Exception:
        frames = []

    # Si no hay GIF, intentar logo estático
    if not frames:
        try:
            logo_pil = Image.open(ASSETS / "logo_impormass.png")
            logo_pil = logo_pil.resize((280, 140), Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(logo_pil)
        except Exception:
            logo_img = None

    # ---------- WIDGETS ----------
    # Título
    tk.Label(root, text="IMPORMASS", font=("Segoe UI", 22, "bold"),
             bg="#ffffff", fg="#007acc").pack(pady=(30, 5))
    tk.Label(root, text="Sistema de Ventas y Almacén", font=("Segoe UI", 11),
             bg="#ffffff", fg="#555555").pack(pady=(0, 15))

    # Imagen (GIF o logo)
    label_img = tk.Label(root, bg="#ffffff")
    label_img.pack(pady=5)

    if frames:
        label_img.configure(image=frames[0])
    elif logo_img:
        label_img.configure(image=logo_img)
        label_img.image = logo_img  # evitar GC

    # Barra de progreso
    bar_frame = tk.Frame(root, bg="#dddddd", width=350, height=10)
    bar_frame.pack(pady=(15, 5))
    bar_frame.pack_propagate(False)
    progress = tk.Frame(bar_frame, bg="#007acc", width=5, height=10)
    progress.place(x=0, y=0)

    tk.Label(root, text="Cargando...", font=("Segoe UI", 9),
             bg="#ffffff", fg="#999999").pack(pady=(2, 10))

    # ---------- ANIMACIÓN ----------
    def animar_gif(i=0):
        if frames and root.winfo_exists():
            label_img.configure(image=frames[i])
            root.after(100, animar_gif, (i + 1) % len(frames))

    def animar_barra(w_val=5):
        if w_val <= 350 and root.winfo_exists():
            progress.place(width=w_val)
            root.after(25, animar_barra, w_val + 8)

    def continuar():
        try:
            root.destroy()
        except Exception:
            pass
        next_fn()

    if frames:
        root.after(50, animar_gif)
    root.after(50, animar_barra)
    root.after(duration_ms, continuar)
    root.mainloop()
