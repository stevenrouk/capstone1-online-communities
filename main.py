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

from src.io_helpers import pickle_obj, load_pickled_obj, get_dataset, create_and_pickle_combined_multigraph
from src.networkx_helpers import combine_graphs

if __name__ == "__main__":
    print("Capstone 1 - Finding Patterns in Social Networks Using Graph Data")
