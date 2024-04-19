import networkx as nx
import random
from time import time

def count_k4_mono(complete_graph):
    """
    Count the number of monochromatic K4 subgraphs in a complete graph.
    :param complete_graph: NetworkX Graph
    :return: int
    """
    counter = 0
    num = len(complete_graph.nodes)
    # Ensure i < j < k < s
    for i in range(num):
        for j in range(i + 1, num):
            for k in range(j + 1, num):
                for s in range(k + 1, num):
                    # Get the subgraph for these four nodes
                    sub_graph_k4 = complete_graph.subgraph([i, j, k, s])
                    # Get the edges of the subgraph
                    sub_graph_k4_edges = nx.get_edge_attributes(sub_graph_k4, 'color')
                    # Check if all edges are either all 0's or all 1's
                    if sum(sub_graph_k4_edges.values()) == 6 or sum(sub_graph_k4_edges.values()) == 0:
                        counter += 1
    return counter

def calculate_probability_edge_color(complete_graph, edge, color=1):
    """
    Calculate the probability of choosing the same color for an edge in the complete graph.
    :param complete_graph: NetworkX Graph
    :param edge: tuple (node1, node2)
    :param color: int (0 or 1)
    :return: float
    """
    prob = 0
    num = len(complete_graph.nodes)
   
    for i in range(num):
        # print((num - i) *  num)
        if i == edge[0] or i == edge[1]:
            continue
        for j in range(i + 1, num):
            if j == edge[0] or j == edge[1]:
                continue
            # Get the subgraph for these four nodes
            sub_graph_k4 = complete_graph.subgraph([i, j, edge[0], edge[1]])
            # Get the edges of the subgraph
            sub_graph_k4_edges = nx.get_edge_attributes(sub_graph_k4, 'color')
            # Check the total edge colors
            if len(sub_graph_k4_edges) == 0:
                prob += 1 / 64
            elif color == 1:
                if len(sub_graph_k4_edges) == sum(sub_graph_k4_edges.values()):
                    prob += 1.0 / pow(2, (6 - len(sub_graph_k4_edges)))
            elif color == 0:
                if sum(sub_graph_k4_edges.values()) == 0:
                    prob += 1.0 / pow(2, (6 - len(sub_graph_k4_edges)))
    return prob

start_time = time()
nodes_num = 30
graph = nx.complete_graph(nodes_num)
leave_edges = list(graph.edges)

# Initialize by coloring one edge randomly
r_index = 0
r_color = 0 if random.random() > 0.5 else 1
graph.add_edge(leave_edges[r_index][0], leave_edges[r_index][1], color=r_color)
leave_edges.remove(leave_edges[r_index])

while leave_edges:
    # start_time = time()
    prob_0 = calculate_probability_edge_color(graph, leave_edges[0], 0)
    prob_1 = calculate_probability_edge_color(graph, leave_edges[0], 1)
    # end_time = time()
    # print(end_time - start_time)
    # Color the edge with the less probable color
    chosen_color = 1 if prob_0 > prob_1 else 0
    graph.add_edge(leave_edges[0][0], leave_edges[0][1], color=chosen_color)
    leave_edges.pop(0)

print(f"Remaining uncolored edges: {len(leave_edges)}")
num_k4 = count_k4_mono(graph)
print(f"{nodes_num} nodes, maximum {nodes_num * (nodes_num - 1) * (nodes_num - 2) * (nodes_num - 3) / (4 * 3 * 2 * 1 * 32)} monochromatic K4 complete graphs, generated graph has {num_k4} monochromatic K4 complete graphs")
end_time = time()
print(f"Elapsed time: {end_time - start_time} seconds")
