import networkx as nx
from pyvis.network import Network

def ensure_html_filename(filename):
    if filename.split('.')[-1] != 'html':
        filename += '.html'
    
    return filename

def create_example_viz(filename):
    filename = ensure_html_filename(filename)

    graph = nx.davis_southern_women_graph()
    create_viz_html(graph, filename)

def create_viz_html(graph, filename):
    filename = ensure_html_filename(filename)

    g_vis = Network()
    g_vis.barnes_hut()
    g_vis.from_nx(graph)
    g_vis.show(filename)
