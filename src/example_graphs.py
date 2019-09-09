def simple_undirected_graph():
    """Returns a dictionary representing an example of an undirected graph."""
    g = {
        'A': ['B'],
        'B': ['A', 'C', 'D'],
        'C': ['B', 'D'],
        'D': ['B', 'C'],
        'E': []
    }

    return g