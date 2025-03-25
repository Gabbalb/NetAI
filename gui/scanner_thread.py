import threading
from core.scanner import scan_generale, scan_dettagliata
from gui.update_handlers import aggiorna_tabella, aggiorna_info_generali


# Questo metodo viene chiamato per avviare una scansione completa in un thread separato.
def avvia_scansione_completa(gui):
    thread = threading.Thread(target=esegui_scansione_completa, args=(gui,))
    thread.daemon = True  # Chiude il thread automaticamente se chiudi la GUI
    thread.start()


# Esegue la scansione generale (ping + gateway)
def esegui_scansione_completa(gui):
    # Avvia la scansione generale (rileva dispositivi attivi, gateway e range)
    attivi, gateway, intervallo = scan_generale()

    # Aggiorna le info generali nella GUI
    gui.root.after(0, lambda: aggiorna_info_generali(gui, gateway, intervallo, attivi))

    # Salva i dati per usarli nella mappa
    gui.devices = attivi
    gui.gateway_ip = gateway
    gui.intervallo_ip = intervallo

    # Avvia la scansione dettagliata per ogni device
    for device in attivi:
        threading.Thread(
            target=esegui_scansione_dettagliata,
            args=(gui, device),
            daemon=True
        ).start()


# Scansione dettagliata (OS, tipo, porte ecc.)
def esegui_scansione_dettagliata(gui, device):
    scan_dettagliata(device)

    # Aggiorna la GUI dopo la scansione dettagliata
    gui.root.after(0, lambda: aggiorna_tabella(gui, device))
