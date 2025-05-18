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

    def ambil_paket_callback():
        engine.start_to_source()

    def antar_paket_callback():
        engine.start_to_destination()

    def stop_callback():
        engine.stop()

    def keluar_callback():
        engine.keluar()

    def run_menu():
        menu = tk.Tk()
        menu.title("Menu Smart Courier")

        tk.Button(menu, text="Load Map", command=load_map_callback).pack(pady=5)
        tk.Button(menu, text="Acak", command=acak_callback).pack(pady=5)
        tk.Button(menu, text="Ambil Paket", command=ambil_paket_callback).pack(pady=5)
        tk.Button(menu, text="Antar Paket", command=antar_paket_callback).pack(pady=5)
        tk.Button(menu, text="Stop", command=stop_callback).pack(pady=5)
        tk.Button(menu, text="Keluar", command=keluar_callback).pack(pady=5)

        menu.mainloop()

    threading.Thread(target=run_menu, daemon=True).start()
