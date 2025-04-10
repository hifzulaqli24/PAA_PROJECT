import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load_map():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            initialdir="maps",
            title="Pilih Peta",
            filetypes=[("Image Files", "*.jpeg *.jpg *.png")]
        )
        root.destroy()
        if file_path:
            engine.load_map_and_random(file_path)

    def acak_posisi():
        engine.randomize_positions()

    def buka_menu():
        menu = tk.Tk()
        menu.title("Menu Smart Courier")

        tk.Button(menu, text="Load Map", command=load_map).pack(pady=5)
        tk.Button(menu, text="Acak", command=acak_posisi).pack(pady=5)

        menu.mainloop()

    threading.Thread(target=buka_menu, daemon=True).start()
