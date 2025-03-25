import nmap
from core.rete import rileva_gateway_e_intervallo
from core.device import Device

scanner = nmap.PortScanner()

def scan_generale():
    # Scopri il gateway e l'intervallo IP da scansionare
    gateway, intervallo = rileva_gateway_e_intervallo()

    dispositivi = []
    print(f"[+] Scansione rapida su: {intervallo}")
    scanner.scan(hosts=intervallo, arguments="-sn")  # solo ping

    for host in scanner.all_hosts():
        if 'mac' in scanner[host]['addresses']:
            mac = scanner[host]['addresses']['mac']
        else:
            mac = "N/A"
        dispositivo = Device(
            ip=host,
            mac=mac,
            hostname=scanner[host].hostname() or "Sconosciuto",
            os="N/D",
            tipo="Dispositivo"
        )
        dispositivi.append(dispositivo)

    return gateway, intervallo, dispositivi

def scan_dettagliata(ip):
    # Scansione approfondita per un singolo host
    risultati = {"mac": "N/A", "hostname": "Sconosciuto", "os": "N/D", "tipo": "Dispositivo"}
    try:
        scanner.scan(hosts=ip, arguments="-O")  # rileva OS
        host_info = scanner[ip]
        risultati["hostname"] = host_info.hostname() or "Sconosciuto"
        if 'osmatch' in host_info and host_info['osmatch']:
            risultati["os"] = host_info['osmatch'][0]['name']
            risultati["tipo"] = deduci_tipo_dispositivo(risultati["os"])
    except Exception as e:
        print(f"[!] Errore nella scansione di {ip}: {e}")
    return risultati

def deduci_tipo_dispositivo(os_name):
    # Prova a indovinare il tipo di dispositivo dal nome dell'OS
    os_name = os_name.lower()
    if "windows" in os_name:
        return "PC"
    if "android" in os_name or "ios" in os_name:
        return "Smartphone"
    if "linux" in os_name and "router" in os_name:
        return "Router"
    if "printer" in os_name:
        return "Stampante"
    return "Dispositivo"
