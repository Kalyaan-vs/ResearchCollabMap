import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load the collaboration data
COLLAB_FILE = "collaborations.csv"
df = pd.read_csv(COLLAB_FILE)

# Sample 100 collaborations for clarity
df_sample = df.sample(n=100, random_state=42)

# Create graph
G_small = nx.Graph()
for _, row in df_sample.iterrows():
    G_small.add_edge(row["Author1"], row["Author2"], weight=row["Collaboration_Count"])

# Remove isolated nodes
G_small.remove_nodes_from(list(nx.isolates(G_small)))

# Increase spacing
pos = nx.spring_layout(G_small, seed=42, k=0.3)

# Draw graph with better spacing & visibility
plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G_small, pos, node_size=100, node_color="blue", alpha=0.7)
nx.draw_networkx_edges(G_small, pos, alpha=0.3, edge_color="gray", width=0.5)

# Label only high-degree nodes
high_degree_nodes = [node for node, degree in dict(G_small.degree()).items() if degree > 2]
nx.draw_networkx_labels(G_small, pos, labels={node: node for node in high_degree_nodes}, font_size=8)

plt.title("Optimized Research Collaboration Network")
plt.show()
