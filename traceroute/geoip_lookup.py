import requests

def get_geo_info(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
        response = requests.get(url, timeout=5)
        data = response.json()

        return {
            "ip": ip or data.get("ip", "N/D"),
            "city": data.get("city", "N/D"),
            "region": data.get("region", "N/D"),
            "country": data.get("country", "N/D"),
            "loc": data.get("loc", "N/D")
        }

    except Exception as e:
        print(f"[ERRORE GEOIP] {ip or 'SELF'} → {e}")
        return {
            "ip": ip or "N/D",
            "city": "N/D",
            "region": "N/D",
            "country": "N/D",
            "loc": "N/D"
        }
