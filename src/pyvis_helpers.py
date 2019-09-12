import random
import numpy as np

import networkx as nx
from pyvis.network import Network

def map_nodes_to_random_colors(nodes):
    """Takes in a list of nodes, and returns a list of colors for those nodes."""
    return [random_color() for _ in nodes]

def map_degrees_to_colors(nodes, graph, how='log'):
    if how == 'linear':
        degrees = [graph.degree(node) for node in nodes]
    elif how == 'log':
        degrees = np.log([graph.degree(node) for node in nodes])
    colors = nums_to_greyscale_hex(degrees)
    
    return colors

def map_nodefunc_to_colors(nodes, nodefunc, how='log'):
    """BROKEN FOR NOW.
    
    Takes in any function that maps nodes to real numbers
    and returns a color gradient mapping from those numbers
    to colors.
    
    Note that nodefunc can be a class method like `graph.degree`.
    """
    nums = np.log([nodefunc(node) for node in nodes])
    colors = nums_to_greyscale_hex(nums)
    
    return colors

def get_pyvis_graph_with_colors(graph=None, color_map_func=map_degrees_to_colors, color_map_func_kwargs={}):
    """Return a pyvis Network graphing object with nodes colored by the mapping function.
    
    With the returned option, you just need to call .show(filename) to show the graph. Example:
    >>> g = get_colorful_graph(graph)
    >>> g.show()
    """
    g = Network(notebook=True)
    
    # Get colors for nodes
    G_nodes = graph.nodes
    G_colors = color_map_func(G_nodes, **color_map_func_kwargs)

    # Add colorful nodes to our pyvis Network object
    for node, color in zip(G_nodes, G_colors):
        g.add_node(node, color=color)

    for edge in graph.edges:
        g.add_edge(*edge)

    return g

def ensure_html_filename(filename):
    if filename.split('.')[-1] != 'html':
        filename += '.html'
    
    return filename

def create_example_viz(filename):
    filename = ensure_html_filename(filename)

    graph = nx.davis_southern_women_graph()
    create_viz_html(graph, filename)

def create_example_viz_2(filename):
    g = Network()
    g.add_nodes(
        [1,2,3],
        value=[10, 100, 400],
        title=["I am node 1", "node 2 here", "and im node 3"],
        x=[21.4, 54.2, 11.2], y=[100.2, 23.54, 32.1],
        label=["NODE 1", "NODE 2", "NODE 3"],
        color=["#00ff1e", "#162347", "#dd4b39"]
    )
    g.show(filename)

def visualize_fast_gnp_random_graph(filename, n=20, p=0.5, seed=None, directed=False):
    G = nx.fast_gnp_random_graph(n, p, seed=seed, directed=directed)
    visualize_random_graph(filename, G)

def get_degree_colors(graph):
    nodes = graph.nodes
    degrees = [graph.degree(node) for node in nodes]
    colors = nums_to_greyscale_hex(degrees)

    return list(zip(nodes, colors))

def visualize_random_graph(filename, graph, color_by_degree=True, notebook=False):
    g = Network(notebook=notebook)
    g.barnes_hut()
    G_nodes = graph.nodes

    # Coloring by degree:
    if color_by_degree:
        G_degrees = [graph.degree(node) for node in G_nodes]
        G_colors = nums_to_greyscale_hex(G_degrees)

        for node, color in zip(G_nodes, G_colors):
            g.add_node(node, color=color)
    
    # Not coloring by degree:
    else:
        for node in G_nodes:
            g.add_node(node)
    
    for edge in graph.edges:
        g.add_edge(*edge)

    g.show(filename)

def create_viz_html(graph, filename):
    filename = ensure_html_filename(filename)

    g_vis = Network()
    g_vis.barnes_hut()
    g_vis.from_nx(graph)
    g_vis.show(filename)

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def rgb_to_hex(rgb_triplet):
    return '#%02x%02x%02x' % rgb_triplet

def nums_to_greyscale_hex(nums, how='linear'):
    """Maps a list of numbers to gradiented red hex colors.
    
    Standardizes all values from 0 to 1 then maps values to
    shades of red based on node degree, with greater degrees
    mapping to brighter red.
    """
    nums = np.array(nums)
    if how == 'log':
        nums = np.log(nums)
    max_nums = max(nums)
    min_nums = min(nums)
    nums_range = max_nums - min_nums
    nums_scaled = (nums - min_nums) / nums_range * 255
    nums_scaled = nums_scaled.astype(int)
    rgb_vals = [(v, 20, 20) for v in nums_scaled]
    hex_vals = [rgb_to_hex(trip) for trip in rgb_vals]

    return hex_vals
