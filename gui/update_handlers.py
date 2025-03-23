ICONE = {
    "Router": "📡",
    "Switch": "🔀",
    "PC": "💻",
    "Smartphone": "📱",
    "Stampante": "🖨️",
    "Dispositivo": "🔘"
}

def aggiorna_tabella(gui, device):
    gui.tree.item(
        device.ip,
        values=(
            device.ip,
            device.mac,
            device.hostname,
            device.os,
            device.tipo,
            ', '.join(device.porte)
        )
    )

def aggiorna_info_generali(gui):
    testo = "\n".join([f"{k.capitalize():<12}: {v}" for k, v in gui.info_generali.items()])
    gui.info_label.config(text=testo)
