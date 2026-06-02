import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("embedding_cache.pkl","rb") as file:
    embedding_cache = pickle.load(file)

words = list(embedding_cache.keys())

embeddings = np.array(
    list(embedding_cache.values())
).astype("float32")

index = faiss.IndexFlatIP(384)
index.add(embeddings)

def semantic_search_faiss(query,top_k=5):
    query_embedding = model.encode(query).astype("float32")
    query_embedding = np.array([query_embedding])
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0],indices[0]):
        results.append((words[idx],float(score)))

    return results

# import time

# start = time.time()

# semantic_search_faiss("happy")

# print(
#     time.time() - start
# )

# print(
#     semantic_search_faiss(
#         "feeling very happy"
#     )
# )

# print(
#     semantic_search_faiss(
#         "machine used for programming"
#     )
# )

# print(
#     semantic_search_faiss(
#         "person who treats patients"
#     )
# )

# print(
#     semantic_search_faiss(
#         "animal that barks"
#     )
# ) 

# print(
#     semantic_search_faiss(
#         "vehicle with two wheels"
#     )
# )

# print(
#     semantic_search_faiss(
#         "place where books are kept"
#     )
# )