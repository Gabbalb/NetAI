import subprocess
import platform

def run_traceroute(dest="8.8.8.8"):
    sistema = platform.system().lower()

    if sistema == "windows":
        cmd = ["tracert", dest]
    else:
        cmd = ["traceroute", dest]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=(sistema == "windows"))
        return result.stdout
    except Exception as e:
        print(f"[ERRORE] Traceroute fallito: {e}")
        return None
