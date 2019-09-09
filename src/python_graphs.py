"""Implementing graphs in plain Python, no extra libraries required."""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Implementing graphs using plain dictionaries and functions.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def example_dict_graph():
    """Returns a dictionary representing an example of an undirected graph."""
    g = {
        'A': ['B'],
        'B': ['A', 'C', 'D'],
        'C': ['B', 'D'],
        'D': ['B', 'C'],
        'E': []
    }

    return g

def num_nodes(g):
    """For a dictionary representation of a graph, returns the number of nodes
    in the graph."""
    return len(g.keys())

def num_edges(g):
    """For a dictionary representation of a graph, returns the number of edges
    in the graph. Assumes the graph is undirected."""
    total_edges_with_duplicates = sum(len(v) for v in g.values())
    return total_edges_with_duplicates // 2

def degree_node(g, node):
    """For a dictionary representation of a graph and the label of a node,
    returns the degree of that node (i.e. the number of other nodes that it
    is connected to)."""
    return len(g[node])

def degree_graph(g):
    """For a dictionary representation of a graph, returns the maximum degree
    of that graph (i.e. the maximum degree of all nodes in the graph)."""
    return max(degree_node(g, node) for node in g)

def adjacency_matrix(g):
    """For a dictionary representation of a graph, returns a list
    representing the adjacency matrix of the graph, where the indices of
    the adjacency matrix are sorted in alphabetical order for strings and
    numerical order for numbers."""
    nodes = sorted(g.keys())
    adj = []
    for row_node in nodes:
        row = []
        for column_node in nodes:
            if column_node in g[row_node]:
                row.append(1)
            else:
                row.append(0)
        adj.append(row)
    
    return adj

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Implementing graphs as a class.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph:
    """Represents a graph with nodes and edges between nodes."""

    def __init__(self, graph_dict):
        self.graph = graph_dict


if __name__ == "__main__":
    g = example_dict_graph()
