import random

import networkx as nx

class RandomSubgraph:

    def __init__(self, graph, starting_node, divisor, attempt_full_graph=False):
        self.graph = graph
        self.graph_to_plot = None # doesn't get generated until we're done with the experiment
        self.random_node_edge_pairs = []
        self.queue = []
        self.exclusions = set()
        self.node = starting_node
        self.divisor = divisor
        self.attempt_full_graph = attempt_full_graph
        self.count = 1
        self._logs = []
    
    def _generate_graph_from_results(self):
        self.graph_to_plot = nx.from_edgelist(self.random_node_edge_pairs, nx.DiGraph)
    
    def run_full(self):
        while True:
            # Sample from our node
            sampled_nodes, new_exclusions = self.randomly_sample_adjacent_nodes(self.node)

            # Update our exclusions
            self.exclusions.update(new_exclusions)

            # Add our sampled nodes to our full list
            self.random_node_edge_pairs.extend(sampled_nodes)

            # Add our new sampled nodes to our queue to sample from in the future
            self.queue.extend([x[1] for x in sampled_nodes])

            # Add the node that we just processed to our exclusion list
            self.exclusions.add(self.node)
            
            self._logs.append({
                "Iteration": self.count,
                "Sampled": len(sampled_nodes),
                "Total sampled so far": len(self.random_node_edge_pairs),
                "Rejected triplets this iteration": len(new_exclusions),
                "Total rejected triplets so far": len(self.exclusions),
                "Queue": len(self.queue)
            })

            self.count += 1
            if self.count % 100 == 0:
                print("Iteration:", self.count)
            try:
                self.node = self.queue.pop()
            except:
                print("Finished after {} iterations.".format(self.count))
                break
        
        self._generate_graph_from_results()
    
    def randomly_sample_adjacent_nodes(self, node):
        # Adjacent nodes to select from, excluding nodes in our exclusion list
        adjacent_nodes = [n for n in list(self.graph[node]) if n not in self.exclusions]
        
        # Randomly select some of those nodes
        random_nodes = random.sample(adjacent_nodes, len(adjacent_nodes) // self.divisor)
        
        # If we're attempting to traverse the full graph, return at least 1 node if possible
        if self.attempt_full_graph:
            if len(adjacent_nodes) > 0 and len(random_nodes) == 0:
                random_nodes = random.sample(adjacent_nodes, 1)
        
        # In the future, we also want to exclude the nodes we didn't choose
        new_exclusions = set(adjacent_nodes) - set(random_nodes)
        
        # Now, we want to get the full edge triplets for our chosen nodes
        # so we can create a new graph from them in the future
        node_edge_weight_triplets = [
            (node, adj_node, self.graph.get_edge_data(node, adj_node))
            for adj_node in random_nodes
        ]
        
        return node_edge_weight_triplets, new_exclusions
