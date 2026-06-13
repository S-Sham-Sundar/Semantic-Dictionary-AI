from collections import deque
import pickle
class GraphEngine:
    def __init__(self):

        with open(
            "semantic_graph.pkl",
            "rb"
        ) as file:

            self.graph = pickle.load(
                file
            )

    def add_edge(self, word1, word2, weight):
            if word1 not in self.graph:
                self.graph[word1] = []
            if word2 not in self.graph:
                self.graph[word2] = []
            self.graph[word1].append((word2, weight))
            self.graph[word2].append((word1, weight))

    def get_synonyms(self, word):
        if word in self.graph:
            return self.graph[word]
        else:
            return []

    def bfs_related_words_depth(self, start_word, max_depth):
        visited = set()
        queue = deque()
        related_words = []
        queue.append((start_word, 0))
        visited.add(start_word)

        while queue:
            current_word, depth = queue.popleft()
            if depth >= max_depth:
                continue
            neighbors = self.get_synonyms(current_word)
            for neighbor, weight in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
                    related_words.append(neighbor)
        return related_words
    

    def get_visualization_data(
        self,
        start_word,
        max_depth=2
    ):

        visited = set()
        queue = deque()

        nodes = []
        edges = []

        queue.append(
            (start_word, 0)
        )

        visited.add(start_word)

        nodes.append({
            "id": start_word,
            "label": start_word
        })

        while queue:

            current_word, depth = queue.popleft()

            if depth >= max_depth:
                continue

            neighbors = self.get_synonyms(
                current_word
            )

            for neighbor, weight in neighbors:

                edges.append({
                    "from": current_word,
                    "to": neighbor,
                    "weight": weight
                })

                if neighbor not in visited:

                    visited.add(neighbor)

                    queue.append(
                        (neighbor, depth + 1)
                    )

                    nodes.append({
                        "id": neighbor,
                        "label": neighbor
                    })

        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def find_path(self, start_word, end_word):
        visited = set()
        queue = deque()
        parent = {}
        queue.append(start_word)
        visited.add(start_word)

        while queue:
            current_word = queue.popleft()
            if current_word == end_word:
                break
            neighbors = self.get_synonyms(current_word)
            for neighbor, weight in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current_word

        if end_word not in visited:
            return []
        
        path = []
        current = end_word

        while current != start_word:
            path.append(current)
            current = parent[current]

        path.append(start_word)
        path.reverse()
        return path

    def bfs_related_words(self, start_word):

        visited = set()
        queue = deque()
        related_words = []

        queue.append(start_word)
        visited.add(start_word)

        while queue:

            current_word = queue.popleft()

            neighbors = self.get_synonyms(current_word)

            for neighbor, weight in neighbors:

                if neighbor not in visited:

                    visited.add(neighbor)

                    queue.append(neighbor)

                    related_words.append(neighbor)

        return related_words



graph = GraphEngine()

print(
    graph.get_synonyms(
        "happy"
    )
)




