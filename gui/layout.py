import tkinter as tk
from tkinter import ttk
from core.info_rete import ottieni_gateway, ottieni_intervallo_rete, ottieni_info_generali
from models.device import Device
from gui.scanner_thread import avvia_scansione_completa
from gui.mappa_canvas import MappaCanvas
from gui.update_handlers import aggiorna_tabella, aggiorna_info_generali

class NetScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NetAI - Scansione di Rete")
        self.devices = []
        self.info_generali = {}
        self.gateway_ip = ""
        self.nodo_attivo = None

        # Layout
        self._crea_layout()

    def _crea_layout(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # === Tab 1: Tabella ===
        self.tab_tabella = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tabella, text="Dispositivi")

        self.info_frame = ttk.LabelFrame(self.tab_tabella, text="Info Generali Rete")
        self.info_frame.pack(fill="x", padx=10, pady=5)

        self.info_label = tk.Label(self.info_frame, justify="left", anchor="w", font=("Consolas", 10))
        self.info_label.pack(padx=10, pady=5, fill="x")

        self.button_frame = ttk.Frame(self.tab_tabella)
        self.button_frame.pack(pady=5)

        self.scan_btn = ttk.Button(self.button_frame, text="Scansiona Rete", command=self._avvia_scansione)
        self.scan_btn.grid(row=0, column=0, padx=5)

        self.tree = ttk.Treeview(
            self.tab_tabella,
            columns=("IP", "MAC", "Hostname", "OS", "Tipo", "Porte"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # === Tab 2: Mappa ===
        self.tab_mappa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mappa, text="Mappa Rete")

        self.canvas = tk.Canvas(self.tab_mappa, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self._trascina_nodo)
        self.canvas.bind("<Button-1>", self._seleziona_nodo)
        self.canvas.bind("<MouseWheel>", self._zoom_canvas)
        self.canvas.bind("<Button-4>", self._zoom_canvas)
        self.canvas.bind("<Button-5>", self._zoom_canvas)

        # Inizializza gestore della mappa
        self.mappa = MappaCanvas(self)

    def _avvia_scansione(self):
        self.scan_btn.config(state="disabled")
        avvia_scansione_completa(self)

    def _seleziona_nodo(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)
        if tags:
            self.nodo_attivo = tags[0]

    def _trascina_nodo(self, event):
        if self.nodo_attivo and self.nodo_attivo in self.mappa.nodi_canvas:
            self.mappa.muovi_nodo(self.nodo_attivo, event.x, event.y)

    def _zoom_canvas(self, event):
        scale = 1.1 if event.delta > 0 or event.num == 4 else 0.9
        self.canvas.scale("all", event.x, event.y, scale, scale)

    # Metodo chiamato da scanner_thread.py
    def aggiorna_gui_post_scan(self):
        aggiorna_info_generali(self)
        self.root.after(200, self.mappa.disegna_grafo)

    def aggiorna_device_gui(self, device):
        aggiorna_tabella(self, device)
        self.mappa.aggiorna_icona(device)
