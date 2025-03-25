import netifaces
import socket
import requests

def rileva_gateway_e_intervallo():
    gateway = netifaces.gateways().get('default', {}).get(netifaces.AF_INET, [None])[0]
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            inet = addrs[netifaces.AF_INET][0]
            if inet.get("addr") and inet.get("addr") != "127.0.0.1":
                ip = inet["addr"]
                netmask = inet.get("netmask", "255.255.255.0")
                subnet = f"{ip}/{_netmask_to_cidr(netmask)}"
                return gateway, subnet
    return gateway, "192.168.1.0/24"

def _netmask_to_cidr(netmask):
    return sum(bin(int(octet)).count("1") for octet in netmask.split("."))

def ottieni_info_generali(gateway, intervallo, attivi):
    try:
        provider = requests.get("https://ipinfo.io/json", timeout=3).json().get("org", "N/D")
    except:
        provider = "N/D"

    return {
        "gateway": gateway or "N/D",
        "intervallo": intervallo,
        "attivi": attivi,
        "provider": provider,
        "ssid": "N/D"  # eventualmente migliorabile in futuro
    }
