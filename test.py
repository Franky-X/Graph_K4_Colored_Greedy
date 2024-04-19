from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

def calculate_score_for_edge(G, edge, current_colorings, potential_color):
    """
    Calculate the change in score if this edge is colored with the potential_color.
    """
    u, v = edge
    # Temporarily color the edge
    current_colorings[(u, v)] = potential_color
    affected_k4s = [sg for sg in combinations(G.nodes(), 4) if u in sg and v in sg]

    score = 0
    for k4 in affected_k4s:
        edge_colors = {tuple(sorted((x, y))): current_colorings.get((x, y), None) 
                       for x, y in combinations(k4, 2)}
        same_color_edges = len([c for c in edge_colors.values() if c == potential_color])
        diff_color_edges = len([c for c in edge_colors.values() if c is not None and c != potential_color])
        
        if diff_color_edges > 0:
            sub_score = 0  # Different colors in K4
        elif same_color_edges == 0:
            sub_score = 2**-5  # No colored edges
        else:
            sub_score = 2**(same_color_edges - 6)  # Same colored edges

        score += sub_score

    # Remove temporary color for the edge
    del current_colorings[(u, v)]

    return score

def greedy_coloring_updated(n):
    G = nx.complete_graph(n)
    colorings = {}  # store the color of edges, initially uncolored

    # Iterate over all edges to color them
    all_edges = list(G.edges())
    while all_edges:
        best_edge = None
        best_color = None
        best_score_increase = float('inf')
        
        # Check each uncolored edge for both colors
        for edge in all_edges:
            if edge not in colorings:
                for color in [0, 1]:
                    score_increase = calculate_score_for_edge(G, edge, colorings, color)
                    if score_increase < best_score_increase:
                        best_score_increase = score_increase
                        best_edge = edge
                        best_color = color

        # Color the best edge with the best color
        colorings[best_edge] = best_color
        all_edges.remove(best_edge)

    # Calculate the number of same-colored K4 subgraphs
    same_colored_K4 = 0
    for subgraph in combinations(G.nodes(), 4):
        subgraph_edges = [tuple(sorted((u, v))) for u, v in combinations(subgraph, 2)]
        if all(colorings.get(edge) == colorings.get(subgraph_edges[0]) for edge in subgraph_edges):
            same_colored_K4 += 1

    return G, colorings, same_colored_K4

# Running the algorithm with n = 5
n = 20

start_time = time.time()  # 记录开始时间
G, colorings, same_colored_K4_count = greedy_coloring_updated(n)
end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算经过时间
print(elapsed_time)
# Theoretical minimum same-colored K4 graphs
theoretical_min_K4 = (n*(n-1)*(n-2)*(n-3)) // (4*3*2*1) // 32

G, colorings, same_colored_K4_count, theoretical_min_K4

print(same_colored_K4_count)
print(theoretical_min_K4)
print("########################")



# Visualizing the graph with updated colored edges
pos = nx.spring_layout(G)  # Generate positions for the nodes

# Extracting edges of each color
edges_color_0 = [(u, v) for (u, v), color in colorings.items() if color == 0]
edges_color_1 = [(u, v) for (u, v), color in colorings.items() if color == 1]

# Drawing the graph
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgrey', edgecolors='black')
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=edges_color_0, edge_color='blue', width=2)
nx.draw_networkx_edges(G, pos, edgelist=edges_color_1, edge_color='red', width=2)

plt.axis('off')
plt.title('Updated Colored Complete Graph $K_5$')
plt.show()

print(same_colored_K4_count)
print(theoretical_min_K4)

# G, colorings, same_colored_K4_count, theoretical_min_K4
