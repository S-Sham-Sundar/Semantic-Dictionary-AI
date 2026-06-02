from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")
def load_vocabulary(filename):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words
vocabulary = load_vocabulary("datasets/words.txt~")
def semantic_search(query):
    query_embedding = model.encode(query)
    similarities = []
    for word in vocabulary:
        word_embedding = model.encode(word)
        score = cosine_similarity(
            [query_embedding],
            [word_embedding]
        )[0][0]
        similarities.append(
            (word, score)
        )
    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )
    return similarities[:5]

import time

start = time.time()

print(
    semantic_search("happy")
)

end = time.time()

print(end - start)
happy = model.encode("happy")
# joyful = model.encode("joyful")
# banana = model.encode("banana")
# Quantum=model.encode("Quantum")
# pancake=model.encode("pancake")
# Syntax=model.encode("Syntax")
# Giraffe=model.encode("Giraffe")

vocabulary = [
    "joyful",
    "banana",
    "cheerful",
    "energetic",
    "sad",
    "apple",
    "Giraffe",
    "Quantum",
    "Syntax",
    "pancake",
]
print(
    "happy vs vocabulary:",
    cosine_similarity([happy], model.encode(vocabulary))
)