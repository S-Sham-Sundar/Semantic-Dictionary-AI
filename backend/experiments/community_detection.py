import pickle
import networkx as nx

with open(
    "semantic_graph.pkl",
    "rb"
) as file:

    graph_data = pickle.load(
        file
    )

G = nx.Graph()

for word, neighbors in graph_data.items():

    for neighbor, score in neighbors:

        G.add_edge(
            word,
            neighbor,
            weight=score
        )

print(
    "Nodes:",
    G.number_of_nodes()
)

print(
    "Edges:",
    G.number_of_edges()
)

from networkx.algorithms.community import (
    greedy_modularity_communities
)

communities = greedy_modularity_communities(
    G
)

print(
    "Communities:",
    len(
        communities
    )
)

for i, community in enumerate(
    list(communities)[:10]
):

    print(
        "\nCommunity",
        i + 1
    )

    print(
        list(community)[:20]
    )