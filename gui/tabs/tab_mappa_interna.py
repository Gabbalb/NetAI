import tkinter as tk
from tkinter import ttk
from gui.mappa_canvas import MappaCanvas

def crea_tab_mappa_interna(gui):
    gui.tab_mappa = ttk.Frame(gui.notebook)
    gui.notebook.add(gui.tab_mappa, text="Mappa Rete")

    gui.canvas = tk.Canvas(gui.tab_mappa, bg="white")
    gui.canvas.pack(fill="both", expand=True)

    gui.canvas.bind("<B1-Motion>", lambda event: _trascina_nodo(gui, event))
    gui.canvas.bind("<Button-1>", lambda event: _seleziona_nodo(gui, event))
    gui.canvas.bind("<MouseWheel>", lambda event: _zoom_canvas(gui, event))
    gui.canvas.bind("<Button-4>", lambda event: _zoom_canvas(gui, event))  # Linux scroll up
    gui.canvas.bind("<Button-5>", lambda event: _zoom_canvas(gui, event))  # Linux scroll down

    gui.mappa = MappaCanvas(gui)

def _seleziona_nodo(gui, event):
    item = gui.canvas.find_closest(event.x, event.y)
    tags = gui.canvas.gettags(item)
    if tags:
        gui.nodo_attivo = tags[0]

def _trascina_nodo(gui, event):
    if gui.nodo_attivo and gui.nodo_attivo in gui.mappa.nodi_canvas:
        gui.mappa.muovi_nodo(gui.nodo_attivo, event.x, event.y)

def _zoom_canvas(gui, event):
    scale = 1.1 if event.delta > 0 or event.num == 4 else 0.9
    gui.canvas.scale("all", event.x, event.y, scale, scale)
