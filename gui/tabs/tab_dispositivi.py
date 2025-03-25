import tkinter as tk
from tkinter import ttk
from gui.scanner_thread import avvia_scansione_completa
from gui.update_handlers import aggiorna_info_generali, aggiorna_tabella

def crea_tab_dispositivi(gui):
    gui.tab_tabella = ttk.Frame(gui.notebook)
    gui.notebook.add(gui.tab_tabella, text="Dispositivi")

    # Info generali
    gui.info_frame = ttk.LabelFrame(gui.tab_tabella, text="Info Generali Rete")
    gui.info_frame.pack(fill="x", padx=10, pady=5)

    gui.info_label = tk.Label(gui.info_frame, justify="left", anchor="w", font=("Consolas", 10))
    gui.info_label.pack(padx=10, pady=5, fill="x")

    # Bottone
    gui.button_frame = ttk.Frame(gui.tab_tabella)
    gui.button_frame.pack(pady=5)

    gui.scan_btn = ttk.Button(gui.button_frame, text="Scansiona Rete", command=lambda: _avvia_scansione(gui))
    gui.scan_btn.grid(row=0, column=0, padx=5)

    # Tabella dispositivi
    gui.tree = ttk.Treeview(
        gui.tab_tabella,
        columns=("IP", "MAC", "Hostname", "OS", "Tipo", "Porte"),
        show="headings"
    )
    for col in gui.tree["columns"]:
        gui.tree.heading(col, text=col)
        gui.tree.column(col, width=130)
    gui.tree.pack(fill="both", expand=True, padx=10, pady=10)

# === CALLBACK ===

def _avvia_scansione(gui):
    gui.scan_btn.config(state="disabled")
    avvia_scansione_completa(gui)



def aggiorna_gui_post_scan(gui):
    aggiorna_info_generali(gui)
    gui.root.after(200, gui.mappa.disegna_grafo)
