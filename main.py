import time

import numpy as np
import pandas as pd

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

if __name__ == "__main__":
    pass
