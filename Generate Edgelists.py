import csv

# Define the edgelists for each conference group
edgelists = {
    "graph1_edgelist.csv": [("author1id", "20", "Graph Drawing"), ("author2id", "35", "IEEE VIS")],
    "graph2_edgelist.csv": [("author1id", "11", "ConfX")],
    "graph3_edgelist.csv": [("author3id", "2", "ConfX")]
}

# Create and save each edgelist as a CSV file
for filename, edges in edgelists.items():
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Conference"])
        writer.writerows(edges)
    print(f"✅ {filename} saved successfully.")
