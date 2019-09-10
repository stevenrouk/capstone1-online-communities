"""Graph creating class for Stanford SNAP Reddit Hyperlink data."""

# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))

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
    """Load graph using NetworkX."""

    def __init__(self):
        pass

    def create_graph(self, filepath):
        start_time = time.time()
        data_loader = DataLoader(filepath=filepath, full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
        node_edge_pairs = data_loader.load()
        print("Data loaded in {} seconds".format(time.time() - start_time))

        start_time = time.time()
        G = nx.DiGraph()
        
        # Initialize loading counter.
        i = 0
        # Could also probably use 'add_edges_from' here: G.add_edges_from(node_edge_pairs[1:])
        for node_from, node_to in node_edge_pairs[1:]:
            # Counter to track progress loading
            if i % 10000 == 0:
                print(i)
            i += 1
            # Add nodes
            G.add_edge(node_from, node_to)
        end_time = time.time()
        print("Data load took {} seconds.".format(end_time - start_time))

        return G
    
    def pickle_graph(self, graph, filename):
        with open(filename, 'wb') as f:
            pickle.dump(graph, f)
    
    def load_pickled_graph(self, filename):
        with open(filename, 'rb') as f:
            graph = pickle.load(f)
        
        return graph
