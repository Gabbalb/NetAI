class Device:
    def __init__(self, ip, hostname, mac):
        self.ip = ip
        self.hostname = hostname
        self.mac = mac
        self.os = 'in analisi...'
        self.porte = []

    def __eq__(self, other):
        return self.ip == other.ip and self.mac == other.mac and self.os == other.os and self.porte == other.porte
