import socket
import netifaces
import subprocess
import re
import ipaddress

def ottieni_gateway():
    gws = netifaces.gateways()
    return gws['default'][netifaces.AF_INET][0]

def ottieni_intervallo_rete():
    hostname = socket.gethostname()
    ip_locale = socket.gethostbyname(hostname)
    rete = ipaddress.IPv4Network(ip_locale + '/24', strict=False)
    return str(rete)

def ottieni_info_generali():
    info = {}

    # IP e subnet
    interfacce = netifaces.interfaces()
    for iface in interfacce:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            ipv4 = addrs[netifaces.AF_INET][0]
            info['ip_locale'] = ipv4.get('addr', 'N/D')
            info['subnet'] = ipv4.get('netmask', 'N/D')
            break

    # Gateway
    info['gateway'] = ottieni_gateway()

    # DNS
    try:
        risultato = subprocess.run("netsh interface ip show dns", capture_output=True, text=True)
        dns = re.findall(r'\d+\.\d+\.\d+\.\d+', risultato.stdout)
        info['dns'] = dns[0] if dns else 'N/D'
    except:
        info['dns'] = 'N/D'

    # SSID – funziona solo se connessi via WiFi
    try:
        risultato = subprocess.run("netsh wlan show interfaces", capture_output=True, text=True)
        match = re.search(r'SSID\s+:\s(.+)', risultato.stdout)
        ssid = match.group(1).strip() if match else None

        # Controlla che non sia vuoto o "N/A"
        if ssid and ssid.upper() != "N/A":
            info['ssid'] = ssid
        else:
            info['ssid'] = 'N/D'
    except:
        info['ssid'] = 'N/D'

    return info
