import matplotlib.pyplot as plt
import networkx as nx

def plot_traceroute_topology(hops_info):
    if not hops_info:
        print("Nessun hop da visualizzare.")
        return

    G = nx.DiGraph()

    # Costruisci grafo con etichette geografiche
    prev_ip = None
    for hop in hops_info:
        ip = hop["ip"]
        label = f"{ip}\n{hop['city']}, {hop['country']}"
        G.add_node(ip, label=label)

        if prev_ip:
            G.add_edge(prev_ip, ip)

        prev_ip = ip

    # Layout semplice (lineare o distribuito)
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, 'label')

    # Disegna il grafo
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, labels=labels,
            node_color='skyblue', node_size=2800,
            font_size=9, font_weight='bold', edge_color='gray', arrows=True)

    plt.title("Topologia Esterna (Traceroute)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
