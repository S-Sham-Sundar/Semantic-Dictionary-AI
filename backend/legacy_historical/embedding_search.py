from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import time
model = SentenceTransformer("all-MiniLM-L6-v2")
with open(
    "embedding_cache.pkl",
    "rb"
) as file:
    embedding_cache = pickle.load(file)

def semantic_search(query):
    query_embedding = model.encode(query)
    similarities = []
    for word, embedding in embedding_cache.items():
        score = cosine_similarity(
            [query_embedding],
            [embedding]
        )[0][0]
        similarities.append(
            (word, float(score))
        )
    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )
    return similarities[:5]



