import tkinter as tk
from tkinter import ttk
import threading
from core.info_rete import ottieni_gateway, ottieni_intervallo_rete, ottieni_info_generali
from models.device import Device
from gui.scanner_thread import avvia_scansione_completa
from gui.mappa_canvas import MappaCanvas
from gui.update_handlers import aggiorna_tabella, aggiorna_info_generali

from traceroute.traceroute_runner import run_traceroute
from traceroute.traceroute_parser import parse_traceroute_output
from traceroute.geoip_lookup import get_geo_info
from traceroute.traceroute_map_geo import plot_geo_traceroute


class NetScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NetAI - Scansione di Rete")
        self.devices = []
        self.info_generali = {}
        self.gateway_ip = ""
        self.nodo_attivo = None

        self._crea_layout()

    def _crea_layout(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # === Tab 1: Dispositivi ===
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

        # === Tab 2: Mappa Rete ===
        self.tab_mappa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mappa, text="Mappa Rete")

        self.canvas = tk.Canvas(self.tab_mappa, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self._trascina_nodo)
        self.canvas.bind("<Button-1>", self._seleziona_nodo)
        self.canvas.bind("<MouseWheel>", self._zoom_canvas)
        self.canvas.bind("<Button-4>", self._zoom_canvas)
        self.canvas.bind("<Button-5>", self._zoom_canvas)

        self.mappa = MappaCanvas(self)

        # === Tab 3: Mappa Esterna ===
        self.tab_traceroute = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_traceroute, text="Mappa Esterna")

        self.traceroute_frame = ttk.Frame(self.tab_traceroute)
        self.traceroute_frame.pack(pady=10)

        self.dest_entry = ttk.Entry(self.traceroute_frame, width=30)
        self.dest_entry.insert(0, "8.8.8.8")
        self.dest_entry.pack(side="left", padx=5)

        self.trace_btn = ttk.Button(self.traceroute_frame, text="Esegui Traceroute", command=self.avvia_traceroute)
        self.trace_btn.pack(side="left", padx=5)

    # === Funzioni scansione locale ===
    def _avvia_scansione(self):
        self.scan_btn.config(state="disabled")
        avvia_scansione_completa(self)

    def aggiorna_gui_post_scan(self):
        aggiorna_info_generali(self)
        self.root.after(200, self.mappa.disegna_grafo)

    def aggiorna_device_gui(self, device):
        aggiorna_tabella(self, device)
        self.mappa.aggiorna_icona(device)

    # === Interazione canvas ===
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

    # === Funzioni Traceroute ===
    def avvia_traceroute(self):
        destinazione = self.dest_entry.get().strip()
        if not destinazione:
            return

        print(f"[Traceroute] Lancio verso {destinazione}...")
        self.trace_btn.config(state="disabled")
        self.root.after(100, lambda: self._esegui_traceroute(destinazione))

    def _esegui_traceroute(self, dest):
        output = run_traceroute(dest)
        if output:
            hops = parse_traceroute_output(output)

            # Aggiungi la tua posizione come primo nodo
            my_info = get_geo_info("")
            my_info["ip"] = "Tu"

            hops_info = [my_info] + [get_geo_info(ip) for ip in hops]
            plot_geo_traceroute(hops_info)
        else:
            print("Traceroute fallito o bloccato.")
        self.trace_btn.config(state="normal")
