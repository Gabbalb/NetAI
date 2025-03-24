import math

ICONE = {
    "Router": "📡",
    "Switch": "🔀",
    "PC": "💻",
    "Smartphone": "📱",
    "Stampante": "🖨️",
    "Dispositivo": "🔘"
}

class MappaCanvas:
    def __init__(self, gui):
        self.gui = gui
        self.canvas = gui.canvas
        self.nodi_canvas = {}  # { ip: [oval_id, label_id] }
        self.linee_canvas = []  # [ (linea_id, ip1, ip2) ]

    def reset_mappa(self):
        self.canvas.delete("all")
        self.nodi_canvas.clear()
        self.linee_canvas.clear()

    def disegna_grafo(self):
        self.reset_mappa()

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w // 2, h // 2
        spacing = 200
        angle_step = 360 / max(len(self.gui.devices), 1)

        # Trova il gateway nella lista dei dispositivi
        gateway = next((d for d in self.gui.devices if d.ip == self.gui.gateway_ip), None)

        # Se non c'è un nodo gateway (es. rete pubblica), disegna i dispositivi senza collegamenti
        if not gateway:
            for i, device in enumerate(self.gui.devices):
                angle = angle_step * i
                rad = angle * math.pi / 180
                x = int(cx + spacing * math.cos(rad))
                y = int(cy + spacing * math.sin(rad))
                self._crea_nodo(device, x, y)
            return  # niente linea da gateway → fine

        # Se gateway esiste, disegna al centro
        self._crea_nodo(gateway, cx, cy)

        # Altri nodi attorno e linee verso il gateway
        count = 0
        for device in self.gui.devices:
            if device.ip == self.gui.gateway_ip:
                continue
            angle = angle_step * count
            rad = angle * math.pi / 180
            x = int(cx + spacing * math.cos(rad))
            y = int(cy + spacing * math.sin(rad))
            self._crea_nodo(device, x, y)
            self._crea_linea(gateway.ip, device.ip)
            count += 1

    def _crea_nodo(self, device, x, y):
        r = 40
        if device.ip == self.gui.gateway_ip:
            colore = "skyblue"
        else:
            colore = "lightgreen" if device.os != 'N/D' else "tomato"

        icon = ICONE.get(device.tipo, "🔘")
        testo = f"{icon}\n{device.hostname}\n{device.ip}"

        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=colore, tags=device.ip)
        label = self.canvas.create_text(x, y, text=testo, font=("Segoe UI Emoji", 9), tags=device.ip)
        self.nodi_canvas[device.ip] = [oval, label]

    def _crea_linea(self, ip1, ip2):
        x1, y1 = self._centro_nodo(ip1)
        x2, y2 = self._centro_nodo(ip2)
        linea = self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
        self.canvas.tag_lower(linea)
        self.linee_canvas.append((linea, ip1, ip2))

    def _centro_nodo(self, ip):
        oval = self.nodi_canvas[ip][0]
        coords = self.canvas.coords(oval)
        x = (coords[0] + coords[2]) // 2
        y = (coords[1] + coords[3]) // 2
        return x, y

    def muovi_nodo(self, ip, x, y):
        if ip in self.nodi_canvas:
            oval, label = self.nodi_canvas[ip]
            r = 40
            self.canvas.coords(oval, x - r, y - r, x + r, y + r)
            self.canvas.coords(label, x, y)
            self._aggiorna_linee()

    def _aggiorna_linee(self):
        for linea, ip1, ip2 in self.linee_canvas:
            x1, y1 = self._centro_nodo(ip1)
            x2, y2 = self._centro_nodo(ip2)
            self.canvas.coords(linea, x1, y1, x2, y2)

    def aggiorna_icona(self, device):
        if device.ip in self.nodi_canvas:
            _, label = self.nodi_canvas[device.ip]
            icon = ICONE.get(device.tipo, "🔘")
            testo = f"{icon}\n{device.hostname}\n{device.ip}"
            self.canvas.itemconfig(label, text=testo)
