import os
import time
import copy

def stampa_tabella_live(devices, info_generali):
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
                porte = ', '.join(d.porte) if d.porte else '-'
                print(f"{d.ip:<16} {d.mac:<20} {d.hostname:<20} {d.os:<30} {porte}")
            print("\nPremi Ctrl+C per terminare.")
            last_state = current_state
        time.sleep(2)
