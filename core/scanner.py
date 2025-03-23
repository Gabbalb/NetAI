import nmap

def scan_network(network_range):
    scanner = nmap.PortScanner()
    print(f"[+] Scansione rapida su: {network_range}")
    scanner.scan(hosts=network_range, arguments='-sn')

    devices = []
    for host in scanner.all_hosts():
        if scanner[host].state() == 'up':
            hostname = scanner[host].hostname()
            mac = scanner[host]['addresses'].get('mac', 'N/A')
            devices.append({
                'ip': host,
                'hostname': hostname or 'Sconosciuto',
                'mac': mac,
            })
    return devices

def scan_dettagliata(device):
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=device.ip, arguments='-T4 -A --osscan-guess')
        host_info = scanner[device.ip]

        os_match = host_info.get('osmatch', [])
        os_name = os_match[0]['name'] if os_match else None

        if not os_name:
            os_class = host_info.get('osclass', [])
            os_name = os_class[0]['osfamily'] if os_class else 'N/D'

        device.os = os_name or 'N/D'

        porte = []
        for proto in ('tcp', 'udp'):
            if proto in host_info:
                for p in host_info[proto]:
                    nome = host_info[proto][p].get('name', '')
                    porte.append(f"{p}/{proto} ({nome})")
        device.porte = porte

        # NEW: tipo riconosciuto
        device.tipo = riconosci_tipo(device)

    except:
        device.os = 'Errore'
        device.porte = []
        device.tipo = 'Dispositivo'

def riconosci_tipo(device):
    mac = device.mac.lower()
    hostname = device.hostname.lower()
    porte = ','.join(device.porte).lower()
    os = device.os.lower()

    if "printer" in hostname or "hp" in mac or "9100" in porte or "631" in porte:
        return "Stampante"
    if "switch" in hostname or "cisco" in mac and not porte:
        return "Switch"
    if "router" in hostname or "gateway" in hostname or "netgear" in mac or "tplink" in mac:
        return "Router"
    if "android" in os or "ios" in os:
        return "Smartphone"
    if "windows" in os or "linux" in os or "mac" in os:
        return "PC"
    return "Dispositivo"
