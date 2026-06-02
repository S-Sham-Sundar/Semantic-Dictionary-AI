import pickle
from collections import deque
with open(
    "semantic_graph.pkl",
    "rb"
) as file:

    graph_data = pickle.load(
        file
    )

total_nodes = len(
    graph_data
)

total_edges = 0

for neighbors in graph_data.values():

    total_edges += len(
        neighbors
    )

average_degree = (
    total_edges /
    total_nodes
)

print(
    "Nodes:",
    total_nodes
)

print(
    "Edges:",
    total_edges
)

print(
    "Average Degree:",
    average_degree
)

from collections import deque

visited = set()

component_count = 0

component_sizes = []

for start_word in graph_data:

    if start_word in visited:
        continue

    component_count += 1

    queue = deque()

    queue.append(
        start_word
    )

    component_size = 0

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(
            current
        )

        component_size += 1

        for neighbor, score in graph_data.get(
            current,
            []
        ):

            if neighbor not in visited:

                queue.append(
                    neighbor
                )

    component_sizes.append(
        component_size
    )

print(
    "Components:",
    component_count
)

print(
    "Largest 10:",
    sorted(
        component_sizes,
        reverse=True
    )[:10]
)