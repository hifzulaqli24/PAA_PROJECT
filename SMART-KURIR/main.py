import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map_callback():
        file = filedialog.askopenfilename(initialdir="maps", title="Pilih Map", filetypes=[("Image Files", "*.jpeg *.jpg *.png")])
        if file:
            engine.load_map(file)

    def acak_callback():
        engine.acak_posisi()

    def mulai_callback():
        if engine.path and len(engine.path) > 1:
            engine.is_moving = True

    def stop_callback():
        engine.stop()

    def keluar_callback():
        engine.keluar()

    def run_menu():
        menu = tk.Tk()
        menu.title("Smart Courier Menu v16")
        for label, func in [
            ("Load Map", load_map_callback),
            ("Acak", acak_callback),
            ("Mulai", mulai_callback),
            ("Stop", stop_callback),
            ("Keluar", keluar_callback),
        ]:
            tk.Button(menu, text=label, width=18, command=func).pack(pady=5)
        menu.mainloop()

    threading.Thread(target=run_menu, daemon=True).start()
