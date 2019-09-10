"""The DirectedGraph class offers basic methods for a directed graph."""

# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))

from src.UndirectedGraph import UndirectedGraph

class DirectedGraph(UndirectedGraph):
    """Represents a directed graph with nodes and edges between nodes."""
    
    def add_node(self, node, adjacent_nodes=[]):
        """Adds a node, and connects it via edges to the nodes in adjacent_nodes."""
        self.graph[node] = list(adjacent_nodes)
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
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
        
        self._refresh_graph()

    def remove_edge(self, node1, node2):
        """Removes an edge between two existing nodes."""
        if node1 not in self.graph or node2 not in self.graph:
            return
        if node2 not in self.graph[node1]:
            return
        
        self.graph[node1].remove(node2)

        self._refresh_graph()
