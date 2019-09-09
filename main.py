import time

import numpy as np

from src.example_graphs import simple_undirected_graph, simple_directed_graph
from src.UndirectedGraph import UndirectedGraph
from src.DirectedGraph import DirectedGraph
from src.DataLoader import DataLoader

if __name__ == "__main__":
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
    # The code as it is currently written takes a while to load for 1000 lines.
    # The efficiency could be immediately improved through changing lists to sets in the classes,
    # where appropriate.
    data_loader = DataLoader(num_lines=10000, cols_to_load=['SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'])
    lines = data_loader.load()

    start_time = time.time()
    reddit_body_hyperlink_graph = DirectedGraph({})
    for line in lines[1:]:
        #print("Working on {}".format(line))
        if line[0] not in reddit_body_hyperlink_graph.nodes:
            #print("ADD NODE: Adding node {} with edge {}".format(line[0], line[1]))
            reddit_body_hyperlink_graph.add_node(line[0], [line[1]])
        elif line[1] not in reddit_body_hyperlink_graph.graph[line[0]]:
            #print("ADD EDGE: Adding edge {} to node {}".format(line[1], line[0]))
            reddit_body_hyperlink_graph.add_edge(line[0], line[1])
        else:
            #print("TODO: ABILITY TO ADD MULTIPLE EDGES")
            #TODO - We want to add multiple edges from one node to another eventually.
            pass
        #input()
    end_time = time.time()
    print("Data load took {} seconds.".format(end_time - start_time))

    start_time = time.time()
    adj = reddit_body_hyperlink_graph.adjacency_matrix()
    end_time = time.time()
    print("Creating the adjacency matrix took {} seconds.".format(end_time - start_time))