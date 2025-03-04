import networkx as nx
import matplotlib.pyplot as plt
import csv


def load_edgelist(filename):
    edges = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            edges.append((row[0], row[1], row[2]))  # Source, Target, Conference
    return edges


def visualize_network(edges, title):
    G = nx.Graph()
    for source, target, conference in edges:
        G.add_edge(source, target, label=conference)

    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=10)
    edge_labels = {(source, target): conference for source, target, conference in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(title)
    plt.show()


# Load and visualize each edgelist
for graph_name in ["graph1_edgelist.csv", "graph2_edgelist.csv", "graph3_edgelist.csv"]:
    edges = load_edgelist(graph_name)
    visualize_network(edges, f"Network for {graph_name}")

