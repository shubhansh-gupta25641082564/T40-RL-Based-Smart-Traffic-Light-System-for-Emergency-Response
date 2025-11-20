import json
from collections import deque

# 1. Define the adjacency graph from your intersection diagram
adj_graph = {
    "N12C1": ["C12C3", "C12W1", "C12C2"],
    "N22C3": ["C32E1", "C32C1", "C32C4"],
    "W12C1": ["C12N1", "C12C3", "C12C2"],
    "E12C3": ["C32N2", "C32C1", "C32C4"],
    "C12C2": ["C22C4", "C22W2", "C22S1"],
    "W22C2": ["C22C1", "C22C4", "C22S1"],
    "E22C4": ["C42C3", "C42C2", "C42S2"],
    "C32C1": ["C12N1", "C12W1", "C12C2"],
    "C22C1": ["C12N1", "C12C3", "C12W1"],
    "C32C4": ["C42E2", "C42C2", "C42S2"],
    "C12C3": ["C32N2", "C32E1", "C32C4"],
    "C42C3": ["C32N2", "C32E1", "C32C1"],
    "C22C4": ["C42C3", "C42E2", "C42S2"],
    "C42C2": ["C22C1", "C22W2", "C22S1"],
    "S12C2": ["C22C1", "C22C4", "C22W2"],
    "S22C4": ["C42C3", "C42E2", "C42C2"],
}

all_nodes = list(adj_graph.keys())
max_depth = 16  # You can increase for longer paths if needed

# 2. Find all possible paths using DFS (no revisiting nodes in a single path)
def dfs_all_paths(graph, start, end, max_depth=16):
    stack = deque([(start, [start])])
    paths = []
    while stack:
        curr, path = stack.pop()
        if curr == end:
            paths.append(path)
        if len(path) < max_depth:
            for neighbor in graph.get(curr, []):
                if neighbor not in path:
                    stack.append((neighbor, path + [neighbor]))
    return paths

# 3. Compute paths for all src-dst pairs (excluding same node)
paths_for_each_pair = {}
for src in all_nodes:
    for dst in all_nodes:
        if src != dst:
            paths = dfs_all_paths(adj_graph, src, dst, max_depth)
            if paths:
                pair_key = f"{src} -> {dst}"
                paths_for_each_pair[pair_key] = paths

# 4. Save results to JSON
with open("all_vehicle_paths.json", "w") as f:
    json.dump(paths_for_each_pair, f, indent=2)

print("✓ All possible multi-hop vehicle paths saved to all_vehicle_paths.json")