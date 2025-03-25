import socket
import netifaces
import platform
import subprocess


def get_ip_locale():
    """Restituisce l'IP locale del dispositivo."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/D"


def get_gateway():
    """Restituisce l'indirizzo IP del gateway predefinito."""
    try:
        gws = netifaces.gateways()
        return gws['default'][netifaces.AF_INET][0]
    except:
        return "N/D"


def get_subnet():
    """Restituisce la subnet mask della rete locale."""
    try:
        iface = get_interface()
        return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
    except:
        return "N/D"


def get_interface():
    """Restituisce il nome dell'interfaccia di rete attiva."""
    ip_locale = get_ip_locale()
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for link in addrs[netifaces.AF_INET]:
                if link.get('addr') == ip_locale:
                    return iface
    return None


def get_dns():
    """Restituisce l'indirizzo IP del server DNS, se disponibile."""
    try:
        gws = netifaces.gateways()
        iface = gws['default'][netifaces.AF_INET][1]
        dns = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [{}])[0].get('addr')
        return dns or "N/D"
    except:
        return "N/D"


def get_ssid():
    """Restituisce l'SSID della rete Wi-Fi (solo se disponibile)."""
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        elif system == "Linux":
            output = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
            return output
        elif system == "Darwin":  # macOS
            output = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
            ).decode()
            for line in output.split("\n"):
                if " SSID" in line:
                    return line.split(":")[1].strip()
    except:
        pass
    return "N/D"
