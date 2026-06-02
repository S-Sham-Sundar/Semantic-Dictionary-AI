import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

with open("embedding_cache.pkl", "rb") as file:
    embedding_cache = pickle.load(file)

words = list(embedding_cache.keys())

embeddings = np.array(list(embedding_cache.values())).astype("float32")

print(len(words))
print(embeddings.shape)

import faiss

index = faiss.IndexFlatIP(384)
index.add(embeddings)
print(index.ntotal)

model = SentenceTransformer("all-MiniLM-L6-v2")
query = "happy"
query_embedding = model.encode(query).astype("float32")

query_embedding = np.array([query_embedding])
scores, indices = index.search(query_embedding, 5)

print("\nScores:")
print(scores)
print("\nIndices:")
print(indices)
print("\nNearest Words:")

for i in indices[0]:
    print(words[i])
