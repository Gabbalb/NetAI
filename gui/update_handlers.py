def aggiorna_info_generali(gui, info):
    # Aggiorna la scritta in alto con le info sulla rete
    gui.info_var.set(info)


def aggiorna_tabella(gui):
    # Cancella e reinserisce tutti i dispositivi nella tabella
    gui.tabella_dispositivi.delete(*gui.tabella_dispositivi.get_children())
    for device in gui.devices:
        gui.tabella_dispositivi.insert("", "end", values=[
            device.ip,
            device.mac,
            device.hostname,
            device.os,
            device.tipo
        ])


def aggiorna_device_gui(gui, device):
    # Aggiorna o aggiunge un singolo dispositivo in tabella e nella mappa
    trovato = False
    for child in gui.tabella_dispositivi.get_children():
        valori = gui.tabella_dispositivi.item(child)['values']
        if valori and valori[0] == device.ip:
            gui.tabella_dispositivi.item(child, values=[
                device.ip, device.mac, device.hostname, device.os, device.tipo
            ])
            trovato = True
            break
    if not trovato:
        gui.tabella_dispositivi.insert("", "end", values=[
            device.ip, device.mac, device.hostname, device.os, device.tipo
        ])

    gui.mappa.aggiorna_icona(device)
