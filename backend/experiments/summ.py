from faiss_search import semantic_search_faiss
from fuzzy_search import load_vocabulary
vocabulary = load_vocabulary(
    "datasets/words.txt~"
)

for i, word in enumerate(vocabulary):

    if word == "dog":

        print(i)

        break