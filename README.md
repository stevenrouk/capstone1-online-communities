# Capstone 1 - Finding Patterns in Social Networks Using Graph Data

Graph analysis of the Stanford SNAP [Social Network: Reddit Hyperlink Network](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) dataset.

## Table of Contents
1. [Motivation](#)
2. [Dataset](#)
3. [Methods](#)
    * [Graph Theory](#)
    * 
2. [Background](#)
    * [Graph Theory](#)
    * []

_(Note: Due the nature of the content in this dataset, there is some inappropriate language shown in some of the graphs.)_

## Motivation

Network data–and more generally graph data—is everywhere.

Google models websites and knowledge as graphs. Facebook models social networks as graphs. Netflix models movie-watchers as graphs. Scientists model molecules and proteins as graphs. Airlines model flights as graphs.

And in this data exploration, we're looking at Reddit hyperlink networks as graphs.

**(insert image of one of my graphs here...but maybe not one of the _best_ ones just yet.)**

With the prevalence of problems that can be viewed as graph problems, I wanted to know how to conduct an analysis on graph data. This isn't an idle interest for me, either. I think that most of the big problems we face today are fundamantally problems of social networks and information flow, problems like: improving our democracies; maintaining freedom of speech while combatting misleading information; connecting people to necessary resources; fighting extreme wealth inequality; creating effective organizations and communities; etc.

By learning how to represent and analyze graphs, I can learn how to help construct a better society for us all.

## The Data

In this project, I worked with the Stanford [Social Network: Reddit Hyperlink Network](https://snap.stanford.edu/data/soc-RedditHyperlinks.html) dataset made available through [SNAP](https://snap.stanford.edu/index.html), the Stanford Network Analysis Platform.

Specifically, this dataset catalogues hyperlinks between subreddits over the course of 2.5 years from January 2014 through April 2017. (A "subreddit" is a community or forum on Reddit dedicated to a specific topic. Subreddits are the basic community structure on Reddit.)

Intuitively, you can think about the data this way:

- Someone posts something on one subreddit: for example, the subreddit "askreddit". This original post can be about anything.
- Someone else links to that post on a different subreddit, essentially sharing the content as something they think the subreddit would find interesting: for example, the original post on "askreddit" could get shared to the subreddit "bestof". This post could be positive ("look at this great post!"), negative ("this post is stupid"), or anywhere in between.

In this dataset, the original post is said to be in the **TARGET** subreddit, and the shared post referencing the TARGET is said to be in the **SOURCE** subreddit. So in our example above, "askreddit" is the TARGET and "bestof" is the SOURCE.

The dataset doesn't include the original post text or who posted it, but it does include a long array of properties about the post text. These properties include:

- Number of words
- Positive and negative sentiment
- 65 [LIWC](http://liwc.wpengine.com/) metrics, such as LIWC_Work, LIWC_Relig, LIWC_Swear, and LIWC_Anger.

The dataset also includes a timestamp, and a label of whether the reposted post is negative or positive/neutral towards the original post.

Here are a few example rows from the data:

**(Insert rows or screenshots or something here.)**

## Terminology

Compared to working with normal tabular or text data, graph data introduced a whole new glossary of terms, topics, and methods that have to be used to discuss the data. This section will provide a brief introduction to the most important terms used in graph theory. Other terms will be defined as needed throughout the README.

These definitions come from (or are adapted from) the Wikipedia page [Glossary of graph theory terms](https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms), which was an invaluable asset during this project. Beneath each definition, there is a description of how the term translates to this specific dataset.

1. **graph.** The fundamental object of study in graph theory, a system of vertices connected in pairs by edges. Often subdivided into directed graphs or undirected graphs according to whether the edges have an orientation or not.
    * _The graph that we're working with is the system of all hyperlinks shared between subreddits over our 2.5 year period._
2. **vertex / node.** A vertex (plural vertices) is (together with edges) one of the two basic units out of which graphs are constructed.
    * _In our dataset, each node is a specific subreddit._
3. **edge.** An edge is (together with vertices) one of the two basic units out of which graphs are constructed. Each edge has two (or in hypergraphs, more) vertices to which it is attached, called its endpoints. Edges may be directed or undirected; undirected edges are also called lines and directed edges are also called arcs or arrows. In an undirected simple graph, an edge may be represented as the set of its vertices, and in a directed simple graph it may be represented as an ordered pair of its vertices.
    * _In our dataset we have directed edges which represent a post in one subreddit (the SOURCE subreddit) that references a post in another subreddit (the TARGET subreddit)._
4. **undirected graph.** An undirected graph is a graph in which the two endpoints of each edge are not distinguished from each other.
    * _In this project, we can create a representation of our graph which is undirected. In the undirected graph representation, edges just show that one of the subreddits has shared from the other (but we don't know which).
5. **directed graph.** A directed graph is one in which the edges have a distinguished direction, from one vertex to another.
    * _The hyperlink sharing graph is fundamentally a directed graph because we have information about one subreddit sharing a post from another. It means something different for subreddit A to share a post from B than for B to share a post from A._
6. **multigraph.** A multigraph is a graph that allows multiple adjacencies. (I.e., a graph where two nodes can have multiple edges running between them.)
    * _Our graph can be represented as a multigraph, where each hyperlink share between two subreddits is another directed edge between those two nodes._
7. **adjacent.** The relation between two vertices that are both endpoints of the same edge. (I.e., if two nodes are connected by an edge they are considered adjacent.)
    * _If two nodes in our dataset are adjacent, then that means one of them has shared a post from the other._
8. **degree.** The degree of a vertex in a graph is its number of incident edges. The degree of a graph G (or its maximum degree) is the maximum of the degrees of its vertices. In a directed graph, one may distinguish the _in-degree_ (number of incoming edges) and _out-degree_ (number of outgoing edges).
    * _The in-degree of a subreddit (node) in our dataset is the number of times that its posts have been referenced in another subreddit. The out-degree of a subreddit is the number of times that it has referenced posts from another subreddit._
9. **network.** A graph in which attributes (e.g. names) are associated with the nodes and/or edges.
    * _We're dealing with a network since our nodes have attributes (e.g. the subreddit name) and our edges have attributes (e.g. the array of text properties, or the timestamp, or the "weight" of an edge (which can mean various things)).

## Representing the Data Computationally

There are multiple ways to represent graphs computationally. For example, simple graphs can be represented as a square matrix where the row and column indices represent the individual nodes, a value of 1 at position (i,j) represents that there is an edge running from node i to node j, and a value of 0 at that position means there isn't. This matrix is usually called the [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix). However, this approach alone isn't sufficient to represent more complicated data, such as networks where the nodes and edges have various attributes.

In the following sections we'll explore how more complex graphs can be represented.

### Non-Graph Representations: Pandas and Python

Before diving into a completely new domain, it can make sense to try your usual tools on the problem. Before I looked at how to represent nodes and edges in a graph-specific data structure, I pulled the data into [pandas](https://pandas.pydata.org/) and looked at some basic statistics.

**(Insert basic pandas results here)**

Although I could have continued analyzing the data in pandas, I wanted to see what interesting analyses came out of graph-specific approaches.

### Custom Graph Class: Python Dictionaries and Classes

Before turning to off-the-shelf libraries, I wanted to see how much progress I could make on my own, using classes and built-in Python data structures. I spent the first day of the project working with toy datasets and building classes to build, navigate, and manipulate graphs.

In Python, you can represent graphs using dictionaries where the keys are nodes and the values are lists of nodes (representing edges). For example, here is a toy undirected graph dataset and its corresponding representation using Python dictionaries:

**(insert photo of toy class, with a caption about there being much doodling on whiteboards)**

And here is the same graph, but now with directed edges:

**(insert photo of toy class, with a caption about there being much doodling on whiteboards)**

The code I used to represent these graphs can be found in the custom class files such as [UndirectedGraph.py](https://github.com/stevenrouk/capstone1-online-communities/blob/master/src/UndirectedGraph.py) and [DirectedGraph.py](https://github.com/stevenrouk/capstone1-online-communities/blob/master/src/DirectedGraph.py).

I did try loading and analyzing the Reddit hyperlink using these custom-built classes, and was able to speed up my load time by 99% by making my classes more efficient.

**(insert photo of improving the efficiency)**

However, as fun as it would have been to completely rebuild graph data structures myself, there are robust and highly efficient libraries that already exist. On the second day of the project, I turned my attention to those.

### NetworkX

[NetworkX](https://networkx.github.io/) is a robust, widely-used library for storing and analyzing graph data in Python, which specific classes for graphs ([Graph](https://networkx.github.io/documentation/stable/reference/classes/graph.html)), directed graphs ([DiGraph](https://networkx.github.io/documentation/stable/reference/classes/digraph.html)), and multigraphs ([MultiDiGraph](https://networkx.github.io/documentation/stable/reference/classes/multidigraph.html)). Using these classes and my custom [DataLoader](https://github.com/stevenrouk/capstone1-online-communities/blob/master/src/DataLoader.py) class, I was able to load the full dataset in under a minute.

Now, NetworkX provided an easy API to access nodes and edges:

**(Show some example code)**

With the graph loaded into NetworkX objects, I was ready to conduct analysis.

## Questions & Answers

For the majority of my analysis, I only worked with connections between nodes, direction of connections between nodes, and numbers of connections between nodes. A big area for future research is bringing in the text properties of the shared posts.

Let's get started!

### Who's the most connected? (Max Degree: In-Degree and Out-Degree)

Results...

### Who's friendly, and who's gossipy? (Sharing Reciprocity)

Results...

### If you start at a random subreddit, where do you end up? (Random Walk Analysis)

Results...

### Which subreddits are the most well-connected? (Centrality and PageRank)

Results...

- Centrality / PageRank (what's the correlation between these two? Could pull this in and do a quick correlation.)

### How do we visualize massive graphs? (Big Graph Data Visualization: Random Node Sampling)

Results...

- Visualizing random subsets of the data
    - Big data visualization - very difficult with graphs, especially, since it's not intuitive how to aggregate nodes
    - I hit upon this idea - what if we were to take a random sample of each node's neighbors
    - Clustering / communities / node aggregation. These are future topics for exploration, but I didn't get to them here.











## Conclusions

Conclusions...

- Takeaways
    - only scratching the surface. this project was really a first attempt at me working with graph data.
    - huge power and potential here.
    - lots of interesting visualization questions

## Future Research

Future research...

## Technologies & Techniques Used

Technologies:
- Python
- pandas
- NumPy
- NetworkX
- pyvis

Techniques:
- Graph Theory
- Network Analysis
- Graph Visualization
- Centrality / PageRank
- Random Walks



