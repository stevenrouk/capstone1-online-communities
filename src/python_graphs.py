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
class BasicGraph:
    """Represents an undirected graph with nodes and edges between nodes."""

    def __init__(self, graph_dict):
        self.graph = graph_dict
        self.nodes = sorted(self.graph.keys())
        self.num_nodes = len(self.nodes)
        self.edges = "Not implemented yet" #TODO
        self.num_edges = sum(len(v) for v in g.values()) // 2
        self.graph_degree = self.degree()
        self.adjacency_matrix = self._create_adjacency_matrix()
    
    def _refresh_graph(self):
        self.nodes = sorted(self.graph.keys())
        self.num_nodes = len(self.nodes)
        self.edges = "Not implemented yet" #TODO
        self.num_edges = sum(len(v) for v in g.values()) // 2
        self.graph_degree = self.degree()
        self.adjacency_matrix = self._create_adjacency_matrix()
    
    def adj(self, node):
        """Returns list of adjacent nodes."""
        return self.graph[node]
    
    def degree(self, node=None):
        """If passed a node label, returns the degree of that node. Otherwise,
        returns the degree of the graph, i.e. the maximum degree of any node
        in the graph."""
        if node:
            return len(self.graph[node])
        else:
            return max(self.degree(node) for node in self.nodes)
    
    def _create_adjacency_matrix(self):
        """Returns a list representing the adjacency matrix of the graph, where
        the indices of the adjacency matrix are sorted in alphabetical order for
        strings and numerical order for numbers."""
        adj = []
        for row_node in self.nodes:
            row = []
            for column_node in self.nodes:
                if column_node in self.graph[row_node]:
                    row.append(1)
                else:
                    row.append(0)
            adj.append(row)
        
        return adj
    
    def add_node(self, node, adjacent_nodes=[]):
        """Adds a node, and connects it via edges to the nodes in adjacent_nodes."""
        self.graph[node] = list(adjacent_nodes)
        for adj_node in adjacent_nodes:
            self.graph[adj_node].append(node)
        self._refresh_graph()
    
    def add_edge(self, node1, node2):
        """Adds an edge between two nodes. If either node doesn't exist, adds it
        to the graph and connects them."""
        # Add nodes if they don't exist.
        if node1 not in self.nodes:
            self.add_node(node1)
        if node2 not in self.nodes:
            self.add_node(node2)
        
        # Update edges.
        if node1 not in self.graph[node2]:
            self.graph[node2].append(node1)
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
        
        self._refresh_graph()
    
    def remove_node(self, node):
        """Removes a node and the corresponding edges."""
        if node not in self.graph:
            return
        del self.graph[node]
        for n in self.graph:
            if node in self.graph[n]:
                self.graph[n].remove(node)
    
        self._refresh_graph()
    
    def remove_edge(self, node1, node2):
        """Removes an edge between two existing nodes."""
        if node1 not in self.graph or node2 not in self.graph:
            return
        if node2 not in self.graph[node1] or node1 not in self.graph[node2]:
            return
        
        self.graph[node1].remove(node2)
        self.graph[node2].remove(node1)

        self._refresh_graph()



if __name__ == "__main__":
    g = example_dict_graph()
    g_class = BasicGraph(g)
