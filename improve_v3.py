from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

def calculate_edge_impact(edge, color, colorings, edge_to_k4s, k4_edges):
    """
    Calculate the impact of coloring an edge on the scores of affected K4s.
    This function returns the difference in total score if this edge were colored with the given color.
    """
    impact = 0
    affected_k4s = edge_to_k4s[edge]
    for k4 in affected_k4s:
        edges = k4_edges[k4]
        colors = [colorings.get(e, -1) for e in edges if e != edge] + [color]
        if all(c == color for c in colors[:-1]):  # All edges same color or uncolored
            impact += 2**(colors.count(color) - 6) - 2**-5
    return impact

def greedy_coloring_v3(n):
    G = nx.complete_graph(n)
    colorings = {}
    edge_to_k4s = {}
    k4_edges = {k4: list(combinations(k4, 2)) for k4 in combinations(G.nodes(), 4)}
    
    for k4, edges in k4_edges.items():
        for edge in edges:
            if edge not in edge_to_k4s:
                edge_to_k4s[edge] = []
            edge_to_k4s[edge].append(k4)

    all_edges = list(G.edges())
    while all_edges:
        best_edge = None
        best_color = None
        best_impact = float('inf')

        # Evaluate the impact of coloring each edge
        for edge in all_edges:
            for color in [0, 1]:
                impact = calculate_edge_impact(edge, color, colorings, edge_to_k4s, k4_edges)
                if impact < best_impact:
                    best_impact = impact
                    best_edge = edge
                    best_color = color

        # Color the edge with the best impact
        colorings[best_edge] = best_color
        all_edges.remove(best_edge)

    # Calculate the number of same-colored K4 subgraphs
    same_colored_K4 = 0
    for k4, edges in k4_edges.items():
        if len(set(colorings[edge] for edge in edges if edge in colorings)) == 1:
            same_colored_K4 += 1

    return G, colorings, same_colored_K4

# Test the further optimized code with a larger n to see performance improvement
n = 8
start_time = time.time()  # 记录开始时间
G_opt_v3, colorings_opt_v3, same_colored_K4_count_opt_v3 = greedy_coloring_v3(n)
end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算经过时间
print(elapsed_time)
# Theoretical minimum same-colored K4 graphs
theoretical_min_K4_opt_v3 = (n*(n-1)*(n-2)*(n-3)) // (4*3*2*1) // 32

G_opt_v3, colorings_opt_v3, same_colored_K4_count_opt_v3, theoretical_min_K4_opt_v3
print(same_colored_K4_count_opt_v3)
print(theoretical_min_K4_opt_v3)
print("########################")