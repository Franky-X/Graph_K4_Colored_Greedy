from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import tqdm
from collections import defaultdict

cnt = 0
n = 20
totol_edges = math.comb(n,2)

def compute_affected_k4s(G, edge):
    """
    Compute the K4 subgraphs affected by coloring the given edge.
    """
    affected_k4s = []
    for neighbor in G.neighbors(edge[0]):
        if neighbor != edge[1]:  # Exclude the other endpoint of the edge
            for k4 in nx.cliques_containing_node(G, nodes=[neighbor], cliques=list(combinations(G.neighbors(neighbor), 3))):
                if edge[0] in k4 and edge[1] in k4:
                    affected_k4s.append(k4)
    return affected_k4s




def optimized_greedy_coloring_v2(n):
    G = nx.complete_graph(n)
    colorings = {}  # store the color of edges
    k4_contributions = {}  # store contribution of each K4 to the score
    edge_to_k4s = {}  # mapping from edge to the K4s it is part of
    colored_k4s = []
    # Precompute all K4 subgraphs and the edges in them
    all_k4s = list(combinations(G.nodes(), 4))
    k4_edges = {k4: list(combinations(k4, 2)) for k4 in all_k4s}

    # Initialize K4 score contributions and edge to K4s mapping
    for k4, edges in k4_edges.items():
        k4_contributions[k4] = 2**-5  # Initial score for uncolored K4
        for edge in edges:
            if edge not in edge_to_k4s:
                edge_to_k4s[edge] = []
            edge_to_k4s[edge].append(k4)

    # Function to update K4 scores when an edge is colored
    def update_k4_scores(edge, color, undo=False):
        set1 = set(tuple(edge_to_k4s[edge]))
        # set2 = set(tuple(colored_k4s))
        affected_k4s = set1

        # print(len(affected_k4s))
        for k4 in affected_k4s:
            edges = k4_edges[k4]
            if undo:  # We need to undo the update (used for temporary scoring)
                k4_contributions[k4] = 2**-5  # Reset to initial state
            else:
                colored_counts = [colorings.get(e, None) for e in edges]
                if any(c is not None and c != color for c in colored_counts):
                    new_score = 0  # Different colors in K4
                else:
                    same_color_count = sum(1 for c in colored_counts if c == color)
                    new_score = 2**(same_color_count - 6) if same_color_count > 0 else 2**-5
                k4_contributions[k4] = new_score

    # def update_k4_scores(edge, color, undo=False):
    #     set1 = edge_to_k4s[edge]
        
    #     for k4 in set1:
    #         edges = k4_edges[k4]
    #         if undo:
    #             k4_contributions[k4] = 2**-5  # Reset to initial state
    #         else:
    #             if any(colorings.get(e) != color for e in edges):
    #                 k4_contributions[k4] = 0  # Score is 0 if there are different colors in K4
    #             else:
    #                 same_color_count = sum(1 for e in edges if colorings.get(e) == color)
    #                 if same_color_count > 0:
    #                     new_score = 2**(same_color_count - 6)
    #                 else:
    #                     new_score = 2**-5
    #                 k4_contributions[k4] = new_score


    # Edge coloring process
    start_time = time.time()  # 记录开始时间
    all_edges = list(G.edges())
    all_colored_edges = []
    color_cnt = []
    color_cnt.append(0)
    color_cnt.append(0)
    sum_up = 0
    edge_color_cnt = 0
    while all_edges:
        best_edge = None
        best_color = None
        lowest_total_score = float('inf')


        # Try coloring each edge
        i = 0
        flag = 0
        for edge in all_edges:
            if edge not in colorings:
                if(color_cnt[0] - color_cnt[1] > 0):
                    order = [1, 0]
                elif(color_cnt[1] - color_cnt[0] > 0):
                    order = [0, 1]
                else:
                    order = [0, 1]         
                # start_time_up = time.time() 
                for color in order:
                    i = i + 1
                    total_score = sum(k4_contributions.values())
                    # print(abs(total_score)/totol_edges)

                    # Temporarily update the score for this coloring
                    
                    update_k4_scores(edge, color)

                    total_score = sum(k4_contributions.values())
                    # print(total_score - lowest_total_score)
                    # print(lowest_total_score)

                    if total_score < lowest_total_score:
                        # if total_score/totol_edges < 2.0:
                        #     # print(abs(total_score)/totol_edges)
                        #     best_edge = edge
                        #     best_color = color
                        #     color_cnt[color] += 1
                        #     flag = 1
                        #     break
                        lowest_total_score = total_score
                        best_edge = edge
                        best_color = color
                        color_cnt[color] += 1
                        colorings[best_edge] = best_color

                        update_k4_scores(best_edge, best_color)  # Permanently update scores

                        # colored_k4s.extend(edge_to_k4s[best_edge])
                        all_edges.remove(best_edge)
                        edge_color_cnt += 1
                        print(str(edge_color_cnt / totol_edges * 100) + "%")
                        print(abs(total_score)/totol_edges)
                        # greedy for optimal timing performance hyperparameter
                        # if total_score/totol_edges < 5: # 50-5.8 100-24.7 20-0.8 150- 56.65
                        #     flag = 1
                        break
                    # else:
                    # # Undo the temporary score update
                    #     update_k4_scores(edge, color, undo=True)
                # end_time_up = time.time()  # 记录结束时间
                # print(end_time_up - start_time_up)
                if(flag == 1):
                    flag = 0
                    break
            sum_up = sum_up + i
            # Color the best edge with the best color

    print(sum_up)
    end_time = time.time()  # 记录结束时间
    # Calculate the number of same-colored K4 subgraphs
    same_colored_K4 = sum(1 for k4 in all_k4s if k4_contributions[k4] > 0)
    elapsed_time = end_time - start_time

    return G, colorings, same_colored_K4, elapsed_time

# Test the optimized code with n = 7


G_opt_v2, colorings_opt_v2, same_colored_K4_count_opt_v2, elapsed_time = optimized_greedy_coloring_v2(n)

# elapsed_time = end_time - start_time  # 计算经过时间
print(elapsed_time)

# Theoretical minimum same-colored K4 graphs
theoretical_min_K4_opt_v2 = (n*(n-1)*(n-2)*(n-3)) // (4*3*2*1) // 32

G_opt_v2, colorings_opt_v2, same_colored_K4_count_opt_v2, theoretical_min_K4_opt_v2

print(same_colored_K4_count_opt_v2)
print(theoretical_min_K4_opt_v2)
print("########################")


pos = nx.spring_layout(G_opt_v2)  # Generate positions for the nodes

# Extracting edges of each color
edges_color_0 = [(u, v) for (u, v), color in colorings_opt_v2.items() if color == 0]
edges_color_1 = [(u, v) for (u, v), color in colorings_opt_v2.items() if color == 1]

# Drawing the graph
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G_opt_v2, pos, node_size=700, node_color='lightgrey', edgecolors='black')
nx.draw_networkx_labels(G_opt_v2, pos)
nx.draw_networkx_edges(G_opt_v2, pos, edgelist=edges_color_0, edge_color='blue', width=2)
nx.draw_networkx_edges(G_opt_v2, pos, edgelist=edges_color_1, edge_color='red', width=2)

plt.axis('off')
plt.title('Updated Colored Complete Graph $K_5$')
plt.show()

# print(same_colored_K4_count)
# print(theoretical_min_K4)

# G, colorings, same_colored_K4_count, theoretical_min_K4
