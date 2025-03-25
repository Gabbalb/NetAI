class Device:
    def __init__(self, ip):
        self.ip = ip
        self.mac = "N/D"
        self.hostname = "Sconosciuto"
        self.os = "in analisi..."
        self.tipo = "Dispositivo"  # default generico
        self.porte = []

    def __repr__(self):
        return f"<Device {self.ip}>"
