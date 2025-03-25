from tkinter import ttk
from traceroute.traceroute_runner import run_traceroute
from traceroute.traceroute_parser import parse_traceroute_output
from traceroute.geoip_lookup import get_geo_info
from traceroute.traceroute_map_geo import plot_geo_traceroute

def crea_tab_mappa_esterna(gui):
    gui.tab_traceroute = ttk.Frame(gui.notebook)
    gui.notebook.add(gui.tab_traceroute, text="Mappa Esterna")

    gui.traceroute_frame = ttk.Frame(gui.tab_traceroute)
    gui.traceroute_frame.pack(pady=10)

    gui.dest_entry = ttk.Entry(gui.traceroute_frame, width=30)
    gui.dest_entry.insert(0, "8.8.8.8")
    gui.dest_entry.pack(side="left", padx=5)

    gui.trace_btn = ttk.Button(
        gui.traceroute_frame,
        text="Esegui Traceroute",
        command=lambda: avvia_traceroute(gui)
    )
    gui.trace_btn.pack(side="left", padx=5)

def avvia_traceroute(gui):
    destinazione = gui.dest_entry.get().strip()
    if not destinazione:
        return

    print(f"[Traceroute] Lancio verso {destinazione}...")
    gui.trace_btn.config(state="disabled")
    gui.root.after(100, lambda: _esegui_traceroute(gui, destinazione))

def _esegui_traceroute(gui, dest):
    output = run_traceroute(dest)
    if output:
        hops = parse_traceroute_output(output)

        # Aggiungi il nodo iniziale (tu) come primo hop
        my_info = get_geo_info("")
        my_info["ip"] = "Tu"

        hops_info = [my_info] + [get_geo_info(ip) for ip in hops]
        # Esegui l'apertura della mappa dopo il ciclo della GUI
        gui.root.after(100, lambda: plot_geo_traceroute(hops_info))

    else:
        print("Traceroute fallito o bloccato.")
    gui.trace_btn.config(state="normal")
