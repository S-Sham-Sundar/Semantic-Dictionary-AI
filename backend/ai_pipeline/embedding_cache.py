from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_vocabulary(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()
    
vocabulary = load_vocabulary("datasets/words.txt~")

embedding_cache = {}

for word in vocabulary:
    embedding_cache[word] = model.encode(word)

# print(len(embedding_cache))

def semantic_search(query):

    query_embedding = model.encode(query)

    similarities = []

    for word, embedding in embedding_cache.items():

        score = cosine_similarity(
            [query_embedding],
            [embedding]
        )[0][0]

        similarities.append(
            (word, score)
        )

    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return similarities[:5]


print(
    semantic_search("happy")
)

