from collections import defaultdict
import random

class RandomWalk:
    
    def __init__(self, graph, current_node=None, silent=True):
        self.steps_taken = 0
        self.blocked = False
        self.graph = graph
        if current_node:
            self.current_node = current_node
        else:
            self.current_node = self.random_node()
        self.nodes_seen = defaultdict(int)
        self.nodes_seen[self.current_node] += 1
        self.silent = silent
    
    def random_node(self):
        nodes = list(self.graph.nodes)
        
        return random.choice(nodes)
    
    def walk(self):
        if self.blocked:
            if not self.silent:
                print("Can't take any more steps.")
        else:
            neighbor_nodes = []
            for neighbor in self.graph.adj[self.current_node]:
                neighbor_weight = self.graph.adj[self.current_node][neighbor]['weight']
                neighbor_nodes.extend([neighbor] * neighbor_weight)
            if neighbor_nodes:
                next_node = random.choice(neighbor_nodes)
                self.current_node = next_node
                self.nodes_seen[self.current_node] += 1
                self.steps_taken += 1
            else:
                self.blocked = True
                if not self.silent:
                    print("Can't take any more steps.")
    
    def delete_graph(self):
        """Method to delete the graph so we aren't using a bunch of memory."""
        self.graph = None