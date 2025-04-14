import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map_callback():
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(
            initialdir="maps",
            title="Pilih Map",
            filetypes=[("Image Files", "*.jpeg *.jpg *.png")]
        )
        root.destroy()
        if filepath:
            engine.load_map(filepath)

    def acak_callback():
        engine.acak_posisi()

    def mulai_callback():
        if engine.path and len(engine.path) > 1:
            engine.is_moving = True
            print("Kurir mulai bergerak...")
        else:
            print("Path tidak tersedia. Klik Acak dulu.")


    def stop_callback():
        engine.stop()

    def keluar_callback():
        engine.keluar()

    def run_menu():
        menu = tk.Tk()
        menu.title("Menu Smart Courier")

        tk.Button(menu, text="Load Map", command=load_map_callback).pack(pady=5)
        tk.Button(menu, text="Acak", command=acak_callback).pack(pady=5)
        tk.Button(menu, text="Mulai", command=mulai_callback).pack(pady=5)
        tk.Button(menu, text="Stop", command=stop_callback).pack(pady=5)
        tk.Button(menu, text="Keluar", command=keluar_callback).pack(pady=5)

        menu.mainloop()

    threading.Thread(target=run_menu, daemon=True).start()
