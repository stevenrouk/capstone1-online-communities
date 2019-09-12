# Modifying the path so we can import from src directory.
import sys
import os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

import pickle

from src.GraphCreator import NetworkXGraphCreator
from src.networkx_helpers import combine_graphs
from src.DataLoader import DataLoader

def pickle_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_pickled_obj(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    
    return obj

def create_and_pickle_combined_digraph():
    networkx_loader = NetworkXGraphCreator()
    G_body = networkx_loader.create_graph(filepath='data/soc-redditHyperlinks-body.tsv')
    G_title = networkx_loader.create_graph(filepath='data/soc-redditHyperlinks-title.tsv')
    G_combined = combine_graphs(G_body, G_title)
    pickle_obj(G_combined, "data_pickle/networkx_digraph_combined.pickle")

def create_and_pickle_combined_multigraph():
    print("loading body data")
    body_data_loader = DataLoader('data/soc-redditHyperlinks-body.tsv', full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    body_data = body_data_loader.load()
    print("body data length:", len(body_data))

    print("loading title data")
    title_data_loader = DataLoader('data/soc-redditHyperlinks-title.tsv', full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    title_data = title_data_loader.load()
    print("title data length:", len(title_data))

    print("creating graphs")
    networkx_loader = NetworkXGraphCreator()
    body_graph = networkx_loader.create_graph(node_edge_pairs=body_data, graph_type='multidigraph')
    print("body graph nodes:", body_graph.number_of_nodes())
    print("body graph edges:", body_graph.number_of_edges())
    title_graph = networkx_loader.create_graph(node_edge_pairs=title_data, graph_type='multidigraph')
    print("title graph nodes:", title_graph.number_of_nodes())
    print("title graph edges:", title_graph.number_of_edges())

    print("combining graphs")
    combined_graph = combine_graphs(body_graph, title_graph)
    print("combined graph nodes:", combined_graph.number_of_nodes())
    print("combined graph edges:", combined_graph.number_of_edges())

    print("pickling combined graph")
    pickle_obj(combine_graphs, "data_pickle/networkx_multigraph_combined.pickle")

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
