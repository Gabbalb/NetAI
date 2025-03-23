import threading
from core.scanner import scan_network, scan_dettagliata
from models.device import Device
from core.info_rete import ottieni_gateway, ottieni_intervallo_rete, ottieni_info_generali


def avvia_scansione_completa(gui):
    gui.devices = []
    gui.mappa.reset_mappa()
    gui.tree.delete(*gui.tree.get_children())

    gui.gateway_ip = ottieni_gateway()
    rete = ottieni_intervallo_rete()
    gui.info_generali = ottieni_info_generali()
    risultati = scan_network(rete)

    for res in risultati:
        device = Device(**res)
        gui.devices.append(device)
        gui.tree.insert(
            "", "end", iid=device.ip,
            values=(device.ip, device.mac, device.hostname, device.os, device.tipo, "")
        )
        threading.Thread(target=esegui_scansione_dettagliata, args=(gui, device), daemon=True).start()

    gui.root.after(100, lambda: attendi_canvas_e_disegna(gui))


def esegui_scansione_dettagliata(gui, device):
    scan_dettagliata(device)
    gui.aggiorna_device_gui(device)


def attendi_canvas_e_disegna(gui):
    if gui.canvas.winfo_width() < 100:
        gui.root.after(100, lambda: attendi_canvas_e_disegna(gui))
    else:
        gui.aggiorna_gui_post_scan()
