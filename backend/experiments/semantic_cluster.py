from backend.faiss_search import semantic_search_faiss

def semantic_cluster(word):

    results = semantic_search_faiss(
        word
    )

    return [
        neighbor
        for neighbor, score
        in results
        if score > 0.6
    ]

print(
    semantic_cluster(
        "happy"
    )
)