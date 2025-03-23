from gui.layout import NetScannerGUI
import tkinter as tk

def avvia_gui():
    root = tk.Tk()
    app = NetScannerGUI(root)
    root.geometry("1000x650")
    root.mainloop()
