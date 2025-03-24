import folium
import webbrowser
import os
import tempfile

def plot_geo_traceroute(hops_info):
    # Posizione di default (centro Europa)
    mappa = folium.Map(location=[48.0, 11.0], zoom_start=3)

    percorso = []

    for hop in hops_info:
        loc = hop.get("loc", None)
        if loc and loc != "N/D":
            lat, lon = map(float, loc.split(","))
            label = f"{hop['ip']}<br>{hop['city']}, {hop['country']}"
            folium.Marker([lat, lon], popup=label, icon=folium.Icon(color='blue')).add_to(mappa)
            percorso.append((lat, lon))

    # Linea che collega i nodi
    if len(percorso) > 1:
        folium.PolyLine(percorso, color="blue", weight=2.5, opacity=0.8).add_to(mappa)

    # Salva mappa temporanea e apri nel browser
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        mappa.save(tmp.name)
        webbrowser.open(f"file://{tmp.name}")
