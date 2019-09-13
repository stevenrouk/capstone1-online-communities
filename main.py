import copy
import pickle
import time

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from src.example_graphs import simple_undirected_graph, simple_directed_graph

from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph
from src.DataLoader import DataLoader
from src.GraphCreator import GraphCreator, NetworkXGraphCreator, NetworkXAttributeGraphCreator
from src.RandomSubgraph import RandomSubgraph

from src.io_helpers import pickle_obj, load_pickled_obj, get_dataset, create_and_pickle_combined_multigraph
from src.networkx_helpers import combine_graphs

if __name__ == "__main__":
    print("Capstone 1 - Finding Patterns in Social Networks Using Graph Data")

    # Here is some example usage of the functions and classes in this repo.

    # Create NetworkX Directed Graph with only edges.
    graph_creator = NetworkXGraphCreator()
    G_body = graph_creator.create_graph(filepath='data/soc-redditHyperlinks-body.tsv')
    G_title = graph_creator.create_graph(filepath='data/soc-redditHyperlinks-title.tsv')
    G = combine_graphs(G_body, G_title)

    print(G.number_of_nodes())

    # Alternatively, if a pickle file is created, simply load that instead.
    # After the first data load, this is the preferred method.
    G = load_pickled_obj('data_pickle/networkx_weighted_full.pickle')

    # Create a random subgraph starting at the node "askreddit".
    random_subgraph = RandomSubgraph(graph=G, starting_node='askreddit', divisor=10)
    random_subgraph.run_full()
    graph_to_plot = random_subgraph.graph_to_plot
