from sentence_transformers import SentenceTransformer
import pickle
model = SentenceTransformer("all-MiniLM-L6-v2")
def load_vocabulary(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()
    
vocabulary = load_vocabulary("datasets/words.txt~")
embedding_cache = {}
for word in vocabulary:
    embedding_cache[word] = model.encode(word)
with open("embedding_cache.pkl", "wb") as file:
        pickle.dump(embedding_cache, file)

print("Embeddings Saved")
print(len(embedding_cache))