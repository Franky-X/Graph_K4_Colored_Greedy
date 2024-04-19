from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

def optimized_greedy_coloring(n):
    G = nx.complete_graph(n)
    colorings = {}  # store the color of edges
    k4_contributions = {}  # store contribution of each K4 to the score

    # Precompute all K4 subgraphs and the edges in them
    all_k4s = list(combinations(G.nodes(), 4))
    k4_edges = {k4: list(combinations(k4, 2)) for k4 in all_k4s}

    # Initialize K4 score contributions (assuming no edges are colored)
    for k4, edges in k4_edges.items():
        k4_contributions[k4] = 2**-5  # Initial score for uncolored K4

    # Define function to update K4 scores when an edge is colored
    def update_k4_scores(edge, color):
        affected_k4s = [k4 for k4 in all_k4s if edge in k4_edges[k4]]
        for k4 in affected_k4s:
            edges = k4_edges[k4]
            colored_counts = [colorings.get(e, None) for e in edges]
            if any(c is not None and c != color for c in colored_counts):
                new_score = 0  # Different colors in K4
            else:
                same_color_count = sum(1 for c in colored_counts if c == color)
                new_score = 2**(same_color_count - 6) if same_color_count > 0 else 2**-5
            k4_contributions[k4] = new_score

    # Edge coloring process
    all_edges = list(G.edges())
    while all_edges:
        best_edge = None
        best_color = None
        best_score_increase = float('inf')

        # Try coloring each edge
        for edge in all_edges:
            if edge not in colorings:
                original_scores = {k4: k4_contributions[k4] for k4 in all_k4s if edge in k4_edges[k4]}
                for color in [0, 1]:
                    # Update scores for trying this color
                    update_k4_scores(edge, color)
                    total_score = sum(k4_contributions.values())
                    if total_score < best_score_increase:
                        best_score_increase = total_score
                        best_edge = edge
                        best_color = color
                    # Revert scores
                    k4_contributions.update(original_scores)

        # Color the best edge with the best color
        colorings[best_edge] = best_color
        update_k4_scores(best_edge, best_color)
        all_edges.remove(best_edge)

    # Calculate the number of same-colored K4 subgraphs
    same_colored_K4 = sum(1 for k4 in all_k4s if k4_contributions[k4] > 0)

    return G, colorings, same_colored_K4

# Test the optimized code with n = 7
n = 20

start_time = time.time()  # 记录开始时间
G_opt, colorings_opt, same_colored_K4_count_opt = optimized_greedy_coloring(n)
end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算经过时间
print(elapsed_time)
# Theoretical minimum same-colored K4 graphs
theoretical_min_K4_opt = (n*(n-1)*(n-2)*(n-3)) // (4*3*2*1) // 32

print(same_colored_K4_count_opt)
print(theoretical_min_K4_opt)
print("########################")

# Visualizing the optimized graph with colored edges

pos_opt = nx.spring_layout(G_opt)  # Generate positions for the nodes



# Extracting edges of each color from optimized coloring

edges_color_0_opt = [(u, v) for (u, v), color in colorings_opt.items() if color == 0]

edges_color_1_opt = [(u, v) for (u, v), color in colorings_opt.items() if color == 1]



# Drawing the graph

plt.figure(figsize=(8, 6))

nx.draw_networkx_nodes(G_opt, pos_opt, node_size=700, node_color='lightgrey', edgecolors='black')

nx.draw_networkx_labels(G_opt, pos_opt)

nx.draw_networkx_edges(G_opt, pos_opt, edgelist=edges_color_0_opt, edge_color='blue', width=2)

nx.draw_networkx_edges(G_opt, pos_opt, edgelist=edges_color_1_opt, edge_color='red', width=2)



plt.axis('off')

plt.title('Optimized Colored Complete Graph $K_7$')

plt.show()