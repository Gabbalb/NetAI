import tkinter as tk
from tkinter import ttk
import threading
import math

from core.scanner import scan_network, scan_dettagliata
from core.info_rete import ottieni_gateway, ottieni_intervallo_rete, ottieni_info_generali
from models.device import Device

# Icone in stile emoji per i tipi
ICONE = {
    "Router": "📡",
    "Switch": "🔀",
    "PC": "💻",
    "Smartphone": "📱",
    "Stampante": "🖨️",
    "Dispositivo": "🔘"
}

class NetScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NetAI - Scansione di Rete")
        self.devices = []
        self.info_generali = {}
        self.gateway_ip = ""

        self.nodi_canvas = {}
        self.linee_canvas = []

        self.crea_layout()

    def crea_layout(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # --- Tab 1: Tabella dispositivi ---
        self.tab_tabella = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tabella, text="Dispositivi")

        self.info_frame = ttk.LabelFrame(self.tab_tabella, text="Info Generali Rete")
        self.info_frame.pack(fill="x", padx=10, pady=5)

        self.info_label = tk.Label(self.info_frame, justify="left", anchor="w", font=("Consolas", 10))
        self.info_label.pack(padx=10, pady=5, fill="x")

        self.button_frame = ttk.Frame(self.tab_tabella)
        self.button_frame.pack(pady=5)

        self.scan_btn = ttk.Button(self.button_frame, text="Scansiona Rete", command=self.avvia_scansione)
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

        # --- Tab 2: Mappa Rete ---
        self.tab_mappa = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_mappa, text="Mappa Rete")

        self.canvas = tk.Canvas(self.tab_mappa, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self.trascina_nodo)
        self.canvas.bind("<Button-1>", self.seleziona_nodo)
        self.canvas.bind("<MouseWheel>", self.zoom_canvas)
        self.canvas.bind("<Button-4>", self.zoom_canvas)
        self.canvas.bind("<Button-5>", self.zoom_canvas)

        self.nodo_attivo = None

    def avvia_scansione(self):
        self.scan_btn.config(state="disabled")
        threading.Thread(target=self.scansione_completa, daemon=True).start()

    def scansione_completa(self):
        self.devices = []
        self.nodi_canvas.clear()
        self.linee_canvas.clear()
        self.canvas.delete("all")
        self.tree.delete(*self.tree.get_children())

        self.gateway_ip = ottieni_gateway()
        rete = ottieni_intervallo_rete()
        self.info_generali = ottieni_info_generali()
        risultati = scan_network(rete)

        for res in risultati:
            device = Device(**res)
            self.devices.append(device)
            self.tree.insert(
                "", "end", iid=device.ip,
                values=(device.ip, device.mac, device.hostname, device.os, device.tipo, "")
            )
            threading.Thread(target=self.aggiorna_dettagli, args=(device,), daemon=True).start()

        self.aggiorna_info_generali()

        def wait_and_draw():
            if self.canvas.winfo_width() < 100:
                self.root.after(100, wait_and_draw)
            else:
                self.disegna_mappa()

        self.root.after(100, wait_and_draw)

    def aggiorna_dettagli(self, device):
        scan_dettagliata(device)
        self.tree.item(
            device.ip,
            values=(device.ip, device.mac, device.hostname, device.os, device.tipo, ', '.join(device.porte))
        )
        self.aggiorna_icona_nodo(device)

    def aggiorna_info_generali(self):
        testo = "\n".join([f"{k.capitalize():<12}: {v}" for k, v in self.info_generali.items()])
        self.info_label.config(text=testo)

    def disegna_mappa(self):
        self.canvas.delete("all")
        self.nodi_canvas.clear()
        self.linee_canvas.clear()

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w // 2, h // 2
        spacing = 200
        angle_step = 360 / max(len(self.devices), 1)

        gateway = next((d for d in self.devices if d.ip == self.gateway_ip), None)
        if gateway:
            self.crea_nodo(gateway, cx, cy)

        raggio = spacing
        count = 0
        for i, d in enumerate(self.devices):
            if d.ip == self.gateway_ip:
                continue
            angle = angle_step * count
            rad = angle * math.pi / 180
            x = int(cx + raggio * math.cos(rad))
            y = int(cy + raggio * math.sin(rad))
            self.crea_nodo(d, x, y)
            self.crea_linea(self.gateway_ip, d.ip)
            count += 1

    def crea_nodo(self, device, x, y):
        r = 40
        if device.ip == self.gateway_ip:
            colore = "skyblue"
        else:
            colore = "lightgreen" if device.os != 'N/D' else "tomato"

        icon = ICONE.get(device.tipo, "🔘")
        testo = f"{icon}\n{device.hostname}\n{device.ip}"

        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=colore, tags=device.ip)
        label = self.canvas.create_text(x, y, text=testo, font=("Segoe UI Emoji", 9), tags=device.ip)
        self.nodi_canvas[device.ip] = [oval, label]

    def crea_linea(self, ip1, ip2):
        x1, y1 = self.centro_nodo(ip1)
        x2, y2 = self.centro_nodo(ip2)
        linea = self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
        self.canvas.tag_lower(linea)
        self.linee_canvas.append((linea, ip1, ip2))

    def centro_nodo(self, ip):
        oval = self.nodi_canvas[ip][0]
        coords = self.canvas.coords(oval)
        x = (coords[0] + coords[2]) // 2
        y = (coords[1] + coords[3]) // 2
        return x, y

    def seleziona_nodo(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)
        if tags:
            self.nodo_attivo = tags[0]

    def trascina_nodo(self, event):
        if self.nodo_attivo and self.nodo_attivo in self.nodi_canvas:
            oval, label = self.nodi_canvas[self.nodo_attivo]
            r = 40
            self.canvas.coords(oval, event.x - r, event.y - r, event.x + r, event.y + r)
            self.canvas.coords(label, event.x, event.y)
            self.aggiorna_linee()

    def aggiorna_linee(self):
        for linea, ip1, ip2 in self.linee_canvas:
            x1, y1 = self.centro_nodo(ip1)
            x2, y2 = self.centro_nodo(ip2)
            self.canvas.coords(linea, x1, y1, x2, y2)

    def aggiorna_icona_nodo(self, device):
        if device.ip in self.nodi_canvas:
            _, label = self.nodi_canvas[device.ip]
            icon = ICONE.get(device.tipo, "🔘")
            testo = f"{icon}\n{device.hostname}\n{device.ip}"
            self.canvas.itemconfig(label, text=testo)

    def zoom_canvas(self, event):
        scale = 1.1 if event.delta > 0 or event.num == 4 else 0.9
        self.canvas.scale("all", event.x, event.y, scale, scale)


def avvia_gui():
    root = tk.Tk()
    app = NetScannerGUI(root)
    root.geometry("1000x650")
    root.mainloop()
