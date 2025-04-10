import tkinter as tk
from tkinter import filedialog
import threading

def start_menu(engine):
    def load(): 
        f = filedialog.askopenfilename(initialdir="maps", title="Pilih Map", filetypes=[("Image Files", "*.jpeg *.jpg *.png")])
        if f: engine.load_map_and_random(f)

    def acak(): engine.randomize_positions()
    def mulai(): 
        if engine.path: 
            engine.is_moving = True

    def stop(): engine.stop()
    def keluar(): engine.keluar()

    def run():
        root = tk.Tk()
        root.title("Smart Courier Menu v15")
        root.geometry("200x220")
        for text, cmd in [("Load Map", load), ("Acak", acak), ("Mulai", mulai), ("Stop", stop), ("Keluar", keluar)]:
            tk.Button(root, text=text, command=cmd, width=18).pack(pady=5)
        root.mainloop()

    threading.Thread(target=run, daemon=True).start()
