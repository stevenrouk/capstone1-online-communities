import copy
import pickle
import time

import numpy as np
import pandas as pd
import networkx as nx

from src.example_graphs import simple_undirected_graph, simple_directed_graph
from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph
from src.DataLoader import DataLoader
from src.GraphCreator import GraphCreator

def main_custom_graph():
    # Create simple undirected graph.
    g = simple_undirected_graph()
    g_class = UndirectedGraph(g)

    # Create simple directed graph.
    g_directed = simple_directed_graph()
    g_directed_class = DirectedGraph(g_directed)

    # Test DirectedGraph class functionality.
    g_directed_class.add_node('F', ('A', 'C'))
    g_directed_class.add_edge('C', 'F')
    g_directed_class.remove_edge('F', 'C')

    # Read in some lines of Reddit Hyperlink data.
    start_time = time.time()
    data_loader = DataLoader(num_lines=1000, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    lines = data_loader.load()

    graph_creator = GraphCreator()
    reddit_body_hyperlink_graph = graph_creator.create_graph(lines)
    graph_creator.pickle_graph(reddit_body_hyperlink_graph, "data_pickle/reddit_body_1000.pickle")
    end_time = time.time()
    print("Time to load and pickle 1000 rows: {}".format(end_time - start_time))

    # Create full pickle file of the non-multigraph Reddit Hyperlink body data.
    start_time = time.time()
    data_loader = DataLoader(full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    lines = data_loader.load()

    graph_creator = GraphCreator()
    reddit_body_hyperlink_graph = graph_creator.create_graph(lines)
    graph_creator.pickle_graph(reddit_body_hyperlink_graph, "data_pickle/reddit_body_full_non_multigraph.pickle")
    end_time = time.time()
    print("Time to load and pickle full file (non-multigraph): {}".format(end_time - start_time))

def value_count_overlap(counts1, counts2, n, return_list=False):
    overlap = set(counts1.head(n).index).intersection(set(counts2.head(n).index))
    if return_list:
        return len(overlap), overlap
    else:
        return len(overlap)

def pandas_analysis():
    df_body = pd.read_csv("data/soc-redditHyperlinks-body.tsv", delimiter='\t')
    df_title = pd.read_csv("data/soc-redditHyperlinks-title.tsv", delimiter='\t')

    # Look at df_body
    print(df_body.info())
    print(df_body.describe())

    # Look at df_body
    print(df_title.info())
    print(df_title.describe())

    # Get post ids from each file.
    title_post_ids = set(df_title['POST_ID'])
    body_post_ids = set(df_body['POST_ID'])

    # Are there any post ids in common? (Nope. We get 0 here.)
    inter = title_post_ids.intersection(body_post_ids)
    print(len(inter))

    # Let's look at the top subreddits by where they're posted.
    body_source_counts = df_body["SOURCE_SUBREDDIT"].value_counts()
    title_source_counts = df_title["SOURCE_SUBREDDIT"].value_counts()

    # Are there commonalities between the two datasets for SOURCE?
    print(set(body_source_counts.head(10).index).intersection(set(title_source_counts.head(10).index)))
    print(set(body_source_counts.head(20).index).intersection(set(title_source_counts.head(20).index)))
    print(set(body_source_counts.head(50).index).intersection(set(title_source_counts.head(50).index)))

    # Let's look at the top subreddits by who they're referencing / posting about.
    body_target_counts = df_body["TARGET_SUBREDDIT"].value_counts()
    title_target_counts = df_title["TARGET_SUBREDDIT"].value_counts()

    # Let's look at the top 10 for each file.
    print(body_target_counts.head(10))
    print(title_target_counts.head(10))

    # Are there commonalities between the two datasets for TARGET?
    print(set(body_target_counts.head(10).index).intersection(set(title_target_counts.head(10).index)))
    print(set(body_target_counts.head(20).index).intersection(set(title_target_counts.head(20).index)))
    print(set(body_target_counts.head(50).index).intersection(set(title_target_counts.head(50).index)))

    # Now let's look at what the top SOURCE and TARGET are for the combined df.
    df_concat = pd.concat([df_body, df_title])
    concat_source_counts = df_concat["SOURCE_SUBREDDIT"].value_counts()
    concat_target_counts = df_concat["TARGET_SUBREDDIT"].value_counts()

    # Let's look at the top 10 for SOURCE and TARGET for the concat df.
    print(concat_source_counts.head(10))
    print(concat_target_counts.head(10))

    # Now let's look at the counts of the overlap with the body and title datasets
    print(value_count_overlap(concat_source_counts, body_source_counts, 10))
    print(value_count_overlap(concat_source_counts, title_source_counts, 10))
    print(value_count_overlap(concat_target_counts, body_target_counts, 10))
    print(value_count_overlap(concat_target_counts, title_target_counts, 10))

def networkx_loading(filepath):
    start_time = time.time()
    data_loader = DataLoader(filepath=filepath, full_file=True, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    node_edge_pairs = data_loader.load()
    print("Data loaded in {} seconds".format(time.time() - start_time))

    start_time = time.time()
    G = nx.DiGraph()
    
    # Initialize loading counter.
    i = 0
    #G.add_edges_from(node_edge_pairs[1:])
    for node_from, node_to in node_edge_pairs[1:]:
        # Counter to track progress loading
        if i % 10000 == 0:
            print(i)
        i += 1
        # Add nodes
        G.add_edge(node_from, node_to)
        # if node_from not in graph.nodes:
        #     graph.add_node(node_from, [node_to])
        # elif node_to not in graph.graph[node_from]:
        #     graph.add_edge(node_from, node_to)
        # else:
        #     # TODO - We want to add multiple edges from one node to another eventually.
        #     pass
    end_time = time.time()
    print("Data load took {} seconds.".format(end_time - start_time))

    return G

def pickle_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_pickled_obj(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    
    return obj

def print_num_nodes_and_edges(G, g_name):
    print(g_name)
    print(G.number_of_nodes())
    print(G.number_of_edges())

if __name__ == "__main__":
    # Load body data.
    #G_body = networkx_loading(filepath='data/soc-redditHyperlinks-body.tsv')
    #pickle_obj(G_body, "data_pickle/networkx_digraph_body.pickle")
    print("Load pickled G_body...")
    G_body = load_pickled_obj("data_pickle/networkx_digraph_body.pickle")

    # Load title data.
    #G_title = networkx_loading(filepath='data/soc-redditHyperlinks-title.tsv')
    #pickle_obj(G_title, "data_pickle/networkx_digraph_title.pickle")
    print("Load pickled G_title...")
    G_title = load_pickled_obj("data_pickle/networkx_digraph_title.pickle")

    #print("Create deepcopy of G_body...")
    #G_combined = copy.deepcopy(G_body)
    #print("Add nodes from G_title...")
    #G_combined.add_nodes_from(G_title)
    #print("Add edges from G_title...")
    #G_combined.add_edges_from(G_title.edges)
    #print("Pickle G_combined...")
    #pickle_obj(G_combined, "data_pickle/networkx_digraph_combined.pickle")

    # Load combined data.
    print("Load pickled G_combined...")
    G_combined = load_pickled_obj("data_pickle/networkx_digraph_combined.pickle")

    for graph, name in zip([G_body, G_title, G_combined], ['G_body', 'G_title', 'G_combined']):
        print_num_nodes_and_edges(graph, name)

    """
    G_body
    35776
    137821

    G_title
    54075
    234792

    G_combined
    67180
    339643

    ...

    (35776 + 54075 - 67180) / 67180
    (137821 + 234792 - 339643) / 339643
    """
