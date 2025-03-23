import nmap
import socket
import ipaddress
import netifaces
import threading
import time
import os
import subprocess
import re
import copy

# Lista dispositivi condivisa
devices = []
info_generali = {}

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

    # SSID (solo se Wi-Fi)
    try:
        risultato = subprocess.run("netsh wlan show interfaces", capture_output=True, text=True)
        match = re.search(r'SSID\s+:\s(.+)', risultato.stdout)
        info['ssid'] = match.group(1).strip() if match else 'N/D'
    except:
        info['ssid'] = 'N/D'

    return info

def scan_network(network_range):
    scanner = nmap.PortScanner()
    print(f"[+] Scansione rapida su: {network_range}")
    scanner.scan(hosts=network_range, arguments='-sn')

    for host in scanner.all_hosts():
        if scanner[host].state() == 'up':
            hostname = scanner[host].hostname()
            mac = scanner[host]['addresses'].get('mac', 'N/A')
            devices.append({
                'ip': host,
                'hostname': hostname if hostname else 'Sconosciuto',
                'mac': mac,
                'os': 'in analisi...',
                'porte': []
            })

def scan_dettagliata(index):
    ip = devices[index]['ip']
    scanner = nmap.PortScanner()
    try:
        scanner.scan(hosts=ip, arguments='-T4 -F')
        host_info = scanner[ip]

        os_match = host_info.get('osmatch', [])
        os_name = os_match[0]['name'] if os_match else 'N/D'
        porte = [f"{p}/tcp ({host_info['tcp'][p]['name']})"
                 for p in host_info.get('tcp', {})]

        devices[index]['os'] = os_name
        devices[index]['porte'] = porte
    except:
        devices[index]['os'] = 'Errore'
        devices[index]['porte'] = []

def stampa_tabella_live():
    last_state = []
    while True:
        current_state = copy.deepcopy(devices)
        if current_state != last_state:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== Info Generali Rete ===")
            for k, v in info_generali.items():
                print(f"{k.capitalize():<12}: {v}")
            print()

            print("=== Rete Rilevata ===")
            print(f"{'IP':<16} {'MAC':<20} {'Hostname':<20} {'OS':<30} {'Porte'}")
            print("-" * 100)
            for d in current_state:
                porte = ', '.join(d['porte']) if d['porte'] else '-'
                print(f"{d['ip']:<16} {d['mac']:<20} {d['hostname']:<20} {d['os']:<30} {porte}")
            print("\nPremi Ctrl+C per terminare.")
            last_state = current_state
        time.sleep(2)

if __name__ == "__main__":
    try:
        gateway = ottieni_gateway()
        rete = ottieni_intervallo_rete()
        info_generali = ottieni_info_generali()
        scan_network(rete)

        for i in range(len(devices)):
            t = threading.Thread(target=scan_dettagliata, args=(i,))
            t.daemon = True
            t.start()

        stampa_tabella_live()

    except KeyboardInterrupt:
        print("\n🔴 Interrotto dall'utente.")