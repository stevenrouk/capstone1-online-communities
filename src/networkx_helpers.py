import copy

import networkx as nx

def max_n_out_degree(graph, n):
    out_degrees = graph.out_degree()
    return sorted(out_degrees, key=lambda x: x[1], reverse=True)[:n]

def max_n_in_degree(graph, n):
    in_degrees = graph.in_degree()
    return sorted(in_degrees, key=lambda x: x[1], reverse=True)[:n]

def max_n_degree(graph, n):
    degree = graph.degree()
    return sorted(degree, key=lambda x: x[1], reverse=True)[:n]

def combine_graphs(graph1, graph2):
    combined_graph = copy.deepcopy(graph1)
    combined_graph.add_nodes_from(graph2)
    combined_graph.add_edges_from(graph2)

    return combined_graph

def top_n_pagerank(graph, n):
    pr = nx.pagerank(graph)
    pr_items = list(pr.items())
    
    return sorted(pr_items, key=lambda x: x[1], reverse=True)[:n]
