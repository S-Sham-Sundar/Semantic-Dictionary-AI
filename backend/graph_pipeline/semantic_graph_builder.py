import time
import pickle
import os

from backend.faiss_search import semantic_search_faiss
from backend.fuzzy_search import load_vocabulary

start = time.time()

vocabulary = load_vocabulary(
    "datasets/words.txt~"
)

# FULL BUILD
# vocabulary = vocabulary

# TEST BUILD
vocabulary = vocabulary

graph_data = {}

for i, word in enumerate(vocabulary):

    if i % 5000 == 0:
        print(
            "Processed:",
            i
        )

    results = semantic_search_faiss(
        word
    )

    graph_data[word] = []

    for neighbor, score in results:

        if neighbor != word:

            graph_data[word].append(
                (neighbor, score)
            )

with open(
    "semantic_graph.pkl",
    "wb"
) as file:

    pickle.dump(
        graph_data,
        file
    )

print(
    "Nodes:",
    len(graph_data)
)

print(
    "Time:",
    time.time() - start
)

print(
    "Graph Size:",
    os.path.getsize(
        "semantic_graph.pkl"
    ) / 1024 / 1024,
    "MB"
)