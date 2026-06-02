# from sentence_transformers import SentenceTransformer
# from embedding_engine import load_vocabulary
# from dictionary_api import get_word_data
# import faiss
# import numpy as np

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )
# vocabulary = load_vocabulary(
#     "datasets/words.txt~"
# )
# vocabulary = vocabulary[:100]

# words = vocabulary
# definitions = []
# valid_words = []

# for word in words:

#     data = get_word_data(word)

#     if not data:
#         continue

#     try:
#         definition = (
#             data[0]
#             ["meanings"][0]
#             ["definitions"][0]
#             ["definition"]
#         )

#         definitions.append(
#             definition
#         )

#         valid_words.append(
#             word
#         )

#     except:
#         pass

# embeddings = model.encode(
#     definitions
# ).astype("float32")

# index = faiss.IndexFlatIP(
#     384
# )

# index.add(
#     embeddings
# )

# query = "animal that barks"

# query_embedding = model.encode(
#     query
# ).astype("float32")

# query_embedding = np.array(
#     [query_embedding]
# )

# scores, indices = index.search(
#     query_embedding,
#     5
# )

# for i in indices[0]:
#     print(
#         valid_words[i]
#     )

from sentence_transformers import SentenceTransformer
from dictionary_api import get_word_data
from fuzzy_search import load_vocabulary

import faiss
import numpy as np
import time

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Load first 100 words
vocabulary = load_vocabulary(
    "datasets/words.txt~"
)

words = vocabulary[38105:38205]

definitions = []
valid_words = []

start = time.time()

for word in words:

    data = get_word_data(word)

    if not data:
        continue

    try:

        definition = (
            data[0]
            ["meanings"][0]
            ["definitions"][0]
            ["definition"]
        )

        definitions.append(
            definition
        )

        valid_words.append(
            word
        )

    except:
        pass

print(
    "Words Processed:",
    len(valid_words)
)

# Create embeddings
embeddings = model.encode(
    definitions
).astype("float32")

print(
    "Embedding Shape:",
    embeddings.shape
)

# Build FAISS index
index = faiss.IndexFlatIP(
    384
)

index.add(
    embeddings
)

print(
    "Vectors Stored:",
    index.ntotal
)

print(
    "Build Time:",
    time.time() - start
)

# TEST 1
query = "animal that barks"

query_embedding = model.encode(
    query
).astype("float32")

query_embedding = np.array(
    [query_embedding]
)

scores, indices = index.search(
    query_embedding,
    5
)

print("\nQuery:", query)

for i in indices[0]:
    print(
        valid_words[i]
    )

# TEST 2
query = "person who treats patients"

query_embedding = model.encode(
    query
).astype("float32")

query_embedding = np.array(
    [query_embedding]
)

scores, indices = index.search(
    query_embedding,
    5
)

print("\nQuery:", query)

for i in indices[0]:
    print(
        valid_words[i]
    )