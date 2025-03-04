import pandas as pd
import networkx as nx
import folium
from itertools import combinations
from geopy.distance import geodesic

# Input & Output Files
INPUT_FILE = "university_locations.csv"
MAP_OUTPUT = "university_collab_map.html"

# Load the existing CSV file (without modifying it)
df = pd.read_csv(INPUT_FILE)

# Convert Latitude and Longitude to numeric (forcing errors to NaN)
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Drop rows with missing (NaN) values
df = df.dropna()

# Check if the dataframe is empty after filtering
if df.empty:
    print("❌ ERROR: No valid university locations found. Please check your CSV file.")
    exit()

# Create a graph
G = nx.Graph()

# Add universities as nodes with their lat/lon
positions = {}
for _, row in df.iterrows():
    uni_name = row["University"]
    lat, lon = row["Latitude"], row["Longitude"]
    positions[uni_name] = (lat, lon)
    G.add_node(uni_name, pos=(lat, lon))

# Create a fully connected graph (every university connected to every other)
for (uni1, uni2) in combinations(G.nodes, 2):
    lat1, lon1 = positions[uni1]
    lat2, lon2 = positions[uni2]
    distance = geodesic((lat1, lon1), (lat2, lon2)).km  # Calculate real-world distance
    G.add_edge(uni1, uni2, weight=distance)

# Use Minimum Spanning Tree (MST) to simplify the graph
MST = nx.minimum_spanning_tree(G, weight="weight")

# Ensure all nodes are connected (if MST fails)
if len(MST.edges) < len(G.nodes) - 1:
    print("⚠️ Some universities are disconnected! Adding extra edges to connect all nodes.")
    remaining_nodes = set(G.nodes) - set(MST.nodes)
    for node in remaining_nodes:
        closest_node = min(MST.nodes, key=lambda x: geodesic(positions[node], positions[x]).km)
        MST.add_edge(node, closest_node, weight=geodesic(positions[node], positions[closest_node]).km)

# Create a Folium Map centered at the first university
first_lat, first_lon = list(G.nodes(data="pos"))[0][1]
m = folium.Map(location=[first_lat, first_lon], zoom_start=3)

# Add markers for universities
for node, pos in positions.items():
    folium.Marker(
        location=[pos[0], pos[1]],
        popup=node,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Add edges (collaboration links) from the Minimum Spanning Tree
for edge in MST.edges:
    lat1, lon1 = positions[edge[0]]
    lat2, lon2 = positions[edge[1]]
    folium.PolyLine(
        locations=[(lat1, lon1), (lat2, lon2)],
        color="red",
        weight=2,
        opacity=0.7
    ).add_to(m)

# Save the map
m.save(MAP_OUTPUT)
print(f"✅ Map saved as '{MAP_OUTPUT}'. Open this file in a browser to view the interactive map.")
