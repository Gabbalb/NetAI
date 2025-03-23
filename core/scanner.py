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
        # OS detection avanzata con guessing
        scanner.scan(hosts=device.ip, arguments='-T4 -A --osscan-guess')
        host_info = scanner[device.ip]

        # Proviamo prima con osmatch
        os_match = host_info.get('osmatch', [])
        os_name = os_match[0]['name'] if os_match else None

        # Se fallisce, proviamo con osclass
        if not os_name:
            os_class = host_info.get('osclass', [])
            os_name = os_class[0]['osfamily'] if os_class else 'N/D'

        device.os = os_name or 'N/D'

        # Porte aperte
        porte = []
        for proto in ('tcp', 'udp'):
            if proto in host_info:
                for p in host_info[proto]:
                    nome = host_info[proto][p].get('name', '')
                    porte.append(f"{p}/{proto} ({nome})")
        device.porte = porte
    except:
        device.os = 'Errore'
        device.porte = []
