# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))

import pickle

from src.GraphCreator import NetworkXGraphCreator
from src.networkx_helpers import combine_graphs

def pickle_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_pickled_obj(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    
    return obj

def create_and_pickle_combined_graph():
    networkx_loader = NetworkXGraphCreator()
    G_body = networkx_loader.create_graph(filepath='data/soc-redditHyperlinks-body.tsv')
    G_title = networkx_loader.create_graph(filepath='data/soc-redditHyperlinks-title.tsv')
    G_combined = combine_graphs(G_body, G_title)
    pickle_obj(G_combined, "data_pickle/networkx_digraph_combined.pickle")

def get_dataset(data_filepath=None, pickle_filepath=None):
    """Gets pickled data if possible, otherwise loads data from the .tsv file.

    Examples:
        >>> G = get_dataset(pickle_filepath='data_pickle/networkx_digraph_body.pickle')

        >>> G = get_dataset(data_filepath='data/soc-redditHyperlinks-body.tsv')
    """
    if pickle_filepath:
        G = load_pickled_obj(pickle_filepath)
    else:
        networkx_loader = NetworkXGraphCreator()
        G = networkx_loader.create_graph(filepath=data_filepath)
    
    return G

if __name__ == "__main__":
    pass
