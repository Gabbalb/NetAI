from core.scanner import scan_network, scan_dettagliata
from core.info_rete import ottieni_gateway, ottieni_intervallo_rete, ottieni_info_generali
from models.device import Device
from core.utils import stampa_tabella_live

import threading

devices = []

if __name__ == "__main__":
    gateway = ottieni_gateway()
    rete = ottieni_intervallo_rete()
    info_generali = ottieni_info_generali()

    # Scansione iniziale
    raw_results = scan_network(rete)
    for result in raw_results:
        devices.append(Device(**result))

    # Avvia scansioni dettagliate in background
    for i in range(len(devices)):
        t = threading.Thread(target=scan_dettagliata, args=(devices[i],))
        t.daemon = True
        t.start()

    stampa_tabella_live(devices, info_generali)
