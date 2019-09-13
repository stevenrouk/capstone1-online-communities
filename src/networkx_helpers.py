import copy
from collections import Counter

import networkx as nx

def max_n_out_degree(graph, n):
    """Finds the top-n nodes by out-degree in a graph.

    Parameters
    ----------
    graph : NetworkX graph object
    n : int
        The number of nodes to return

    Returns
    -------
    list
        A list of n nodes from the graph with the top out-degrees.
    """
    out_degrees = graph.out_degree()
    return sorted(out_degrees, key=lambda x: x[1], reverse=True)[:n]

def max_n_in_degree(graph, n):
    """Finds the top-n nodes by in-degree in a graph.

    Parameters
    ----------
    graph : NetworkX graph object
    n : int
        The number of nodes to return

    Returns
    -------
    list
        A list of n nodes from the graph with the top in-degrees.
    """
    in_degrees = graph.in_degree()
    return sorted(in_degrees, key=lambda x: x[1], reverse=True)[:n]

def max_n_degree(graph, n):
    """Finds the top-n nodes by total degree in a graph.

    Parameters
    ----------
    graph : NetworkX graph object
    n : int
        The number of nodes to return

    Returns
    -------
    list
        A list of n nodes from the graph with the top total degrees.
    """
    degree = graph.degree()
    return sorted(degree, key=lambda x: x[1], reverse=True)[:n]

def combine_graphs(graph1, graph2):
    """Takes two NetworkX graphs and returns a combined graph with all
    nodes and edges from each graph.

    Parameters
    ----------
    graph1 : NetworkX graph object
    graph2 : NetworkX graph object

    Returns
    -------
    NetworkX graph object
        A graph with all nodes and edges from both graphs
    """
    combined_graph = copy.deepcopy(graph1)
    combined_graph.add_nodes_from(graph2)
    combined_graph.add_edges_from(graph2.edges)

    return combined_graph

def top_n_pagerank(graph, n):
    """Finds the top-n nodes by PageRank in a graph.

    Parameters
    ----------
    graph : NetworkX graph object
    n : int
        The number of nodes to return

    Returns
    -------
    list
        A list of n nodes from the graph with the top PageRank.
    """
    pr = nx.pagerank(graph)
    pr_items = list(pr.items())
    
    return sorted(pr_items, key=lambda x: x[1], reverse=True)[:n]

def get_component_length_counts(graph):
    """Returns the counts of the lengths (i.e. number of nodes) of each component.

    Parameters
    ----------
    graph : NetworkX graph object

    Returns
    -------
    Counter
        A Counter object with the counts of the lengths of the components
    """
    graph_undirected = graph.to_undirected()
    connected_components_list = list(nx.connected_components(graph_undirected))
    
    return Counter([len(component) for component in connected_components_list])

def connected_components_of_degree_n(graph, n):
    graph_undirected = graph.to_undirected()
    connected_components_list = list(nx.connected_components(graph_undirected))

    return [c for c in connected_components_list if len(c) == n]

def create_subgraph_from_node_and_ins_outs(graph, n):
    subgraph = nx.DiGraph()
    subgraph.add_edges_from(graph.in_edges(n))
    subgraph.add_edges_from(graph.out_edges(n))

    return subgraph