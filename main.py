import numpy as np

from src.example_graphs import simple_undirected_graph, simple_directed_graph
from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph

if __name__ == "__main__":
    g = simple_undirected_graph()
    g_class = UndirectedGraph(g)

    g_directed = simple_directed_graph()
    g_directed_class = DirectedGraph(g_directed)

    g_directed_class.add_node('F', ('A', 'C'))
    g_directed_class.add_edge('C', 'F')
    print(np.array(g_directed_class.adjacency_matrix))
    g_directed_class.remove_edge('F', 'C')
    print(np.array(g_directed_class.adjacency_matrix))
    print(g_directed_class.graph)
