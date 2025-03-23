import networkx as nx
import matplotlib.pyplot as plt

def disegna_grafo(devices, gateway_ip):
    G = nx.Graph()

    # Aggiungi il nodo del gateway
    G.add_node(gateway_ip, label="Gateway", color="skyblue")

    for d in devices:
        if d.ip != gateway_ip:
            label = f"{d.hostname}\n{d.ip}"
            colore = "lightgreen" if d.os != 'N/D' else "lightcoral"
            G.add_node(d.ip, label=label, color=colore)
            G.add_edge(gateway_ip, d.ip)

    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, 'label')
    colors = [G.nodes[n].get('color', 'gray') for n in G.nodes]

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=1800, font_size=8, edge_color="gray")
    nx.draw_networkx_labels(G, pos, labels, font_size=9)
    plt.title("Topologia della Rete")
    plt.axis('off')
    plt.show()
