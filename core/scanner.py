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
        scanner.scan(hosts=device.ip, arguments='-T4 -F')
        host_info = scanner[device.ip]

        os_match = host_info.get('osmatch', [])
        os_name = os_match[0]['name'] if os_match else 'N/D'
        porte = [f"{p}/tcp ({host_info['tcp'][p]['name']})"
                 for p in host_info.get('tcp', {})]

        device.os = os_name
        device.porte = porte
    except:
        device.os = 'Errore'
        device.porte = []
