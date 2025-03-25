
from tkinter import Frame, Label, StringVar, ttk
from gui.mappa_canvas import MappaCanvas
from gui.update_handlers import aggiorna_info_generali, aggiorna_tabella

class NetScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NetAI - Network Topology Scanner")

        self.gateway_ip = None
        self.intervallo_ip = None
        self.devices = []

        # === Area superiore con info generali sulla rete
        self.info_var = StringVar()
        self.info_var.set("Informazioni di rete in attesa di scansione...")
        Label(root, textvariable=self.info_var, anchor="w").pack(fill="x", padx=10, pady=(5, 0))

        # === Tabella dispositivi
        self.tabella_dispositivi = ttk.Treeview(root, columns=("IP", "MAC", "Host", "OS", "Tipo"), show="headings")
        for col in ("IP", "MAC", "Host", "OS", "Tipo"):
            self.tabella_dispositivi.heading(col, text=col)
            self.tabella_dispositivi.column(col, width=120)
        self.tabella_dispositivi.pack(fill="both", expand=True, padx=10, pady=5)

        # === Canvas per la mappa della rete
        self.canvas = ttk.Frame(root)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)
        self.canvas = self.canvas  # compatibilità
        self.canvas = self._crea_canvas_widget()

        self.mappa = MappaCanvas(self)

    def _crea_canvas_widget(self):
        from tkinter import Canvas
        canvas = Canvas(self.root, bg="white")
        canvas.pack(fill="both", expand=True)
        return canvas

    def aggiorna_gui_post_scan(self):
        from core.rete import ottieni_info_generali

        # Aggiorna info in alto e tabella dispositivi, poi ridisegna la mappa
        info = ottieni_info_generali(self.gateway_ip, self.intervallo_ip, self.devices)
        aggiorna_info_generali(self, info)
        aggiorna_tabella(self)
        self.mappa.disegna_grafo()
