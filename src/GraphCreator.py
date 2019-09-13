"""Graph creating class for Stanford SNAP Reddit Hyperlink data."""

# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

import time
import numpy as np
import pickle

import networkx as nx

from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph
from src.DataLoader import DataLoader


class GraphCreator:
    """Load graph using custom graph class."""

    def __init__(self):
        pass

    def create_graph(self, node_edge_pairs=[]):
        start_time = time.time()
        graph = DirectedGraph({})
        
        # Initialize loading counter.
        i = 0

        for node_from, node_to in node_edge_pairs[1:]:
            
            # Counter to track progress loading
            if i % 100 == 0:
                print(i)
            i += 1

            if node_from not in graph.nodes:
                graph.add_node(node_from, [node_to])
            elif node_to not in graph.graph[node_from]:
                graph.add_edge(node_from, node_to)
            else:
                # TODO - We want to add multiple edges from one node to another eventually.
                pass
        end_time = time.time()
        print("Data load took {} seconds.".format(end_time - start_time))

        return graph
    
    def pickle_graph(self, graph, filename):
        with open(filename, 'wb') as f:
            pickle.dump(graph, f)
    
    def load_pickled_graph(self, filename):
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        
        return graph

class NetworkXGraphCreator:
    """Load graph using NetworkX (without attributes)."""

    def __init__(self):
        pass

    def create_graph(self, node_edge_pairs=[], filepath=None, graph_type='digraph'):
        if len(node_edge_pairs) == 0:
            start_time = time.time()
            data_loader = DataLoader(filepath=filepath, full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
            node_edge_pairs = data_loader.load()
            print("Data load from file took {} seconds".format(time.time() - start_time))

        start_time = time.time()
        if graph_type == 'digraph':
            G = nx.DiGraph()
        elif graph_type == 'multidigraph':
            G = nx.MultiDiGraph()
        
        # Initialize loading counter.
        i = 1
        # Could also probably use 'add_edges_from' here: G.add_edges_from(node_edge_pairs[1:])
        for node_from, node_to in node_edge_pairs[1:]:
            # Counter to track progress loading
            if i % 10000 == 0:
                print(i)
            i += 1
            # Add nodes
            G.add_edge(node_from, node_to)
        end_time = time.time()
        print("Data load into graph took {} seconds.".format(end_time - start_time))

        return G
    
    def pickle_graph(self, graph, filename):
        with open(filename, 'wb') as f:
            pickle.dump(graph, f)
    
    def load_pickled_graph(self, filename):
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        
        return graph

class NetworkXAttributeGraphCreator:
    """Load graph using NetworkX (with attributes)."""

    def __init__(self):
        pass

    def create_graph(self, node_edge_attrs=[], attr_names=[], cols_to_load=[], filepath=None, graph_type='digraph'):
        """Expects to be passed a list of iterables where the first index holds the first node,
        the second index holds the second node, and the rest of the indices (if they exist) hold
        attribute data for the edge.
        
        If attributes are included in node_edge_attrs, then attr_names is also expected."""
        start_time = time.time()
        if graph_type == 'digraph':
            G = nx.DiGraph()
        elif graph_type == 'multidigraph':
            G = nx.MultiDiGraph()
        
        # Initialize loading counter.
        i = 1
        # Could also probably use 'add_edges_from' here: G.add_edges_from(node_edge_pairs[1:])
        for node_from, node_to, *attributes in node_edge_attrs[1:]:
            # Counter to track progress loading
            if i % 10000 == 0:
                print(i)
            i += 1
            # Add nodes
            G.add_edge(node_from, node_to, **dict(zip(attr_names, attributes)))
        end_time = time.time()
        print("Data load into graph took {} seconds.".format(end_time - start_time))

        return G
    
    def pickle_graph(self, graph, filename):
        with open(filename, 'wb') as f:
            pickle.dump(graph, f)
    
    def load_pickled_graph(self, filename):
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        
        return graph
