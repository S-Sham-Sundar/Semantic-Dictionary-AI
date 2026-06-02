from collections import deque
import pickle

with open(
    "semantic_graph.pkl",
    "rb"
) as file:

    graph_data = pickle.load(
        file
    )

def semantic_explore(
    word,
    max_depth=3
):

    visited = set()

    queue = deque()

    results = []

    queue.append(
        (word, 0)
    )

    visited.add(
        word
    )

    while queue:

        current_word, depth = queue.popleft()

        results.append(
            (
                current_word,
                depth
            )
        )

        if depth >= max_depth:
            continue

        for neighbor, score in graph_data.get(
            current_word,
            []
        ):

            if neighbor not in visited:

                visited.add(
                    neighbor
                )

                queue.append(
                    (
                        neighbor,
                        depth + 1
                    )
                )

    return results


if __name__ == "__main__":

    results = semantic_explore(
        "computer",
        3
    )

    for word, depth in results:

        print(
            f"Depth {depth}: {word}"
        )