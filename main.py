import numpy as np

from src.example_graphs import simple_undirected_graph, simple_directed_graph
from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph

if __name__ == "__main__":
    # Create simple undirected graph.
    g = simple_undirected_graph()
    g_class = UndirectedGraph(g)

    # Create simple directed graph.
    g_directed = simple_directed_graph()
    g_directed_class = DirectedGraph(g_directed)

    # Test DirectedGraph class functionality.
    g_directed_class.add_node('F', ('A', 'C'))
    g_directed_class.add_edge('C', 'F')
    g_directed_class.remove_edge('F', 'C')

    
