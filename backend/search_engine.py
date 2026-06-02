from backend.trie import Trie
from backend.fuzzy_search import find_closest_words, load_vocabulary
from backend.graph_engine import GraphEngine
from backend.faiss_search import semantic_search_faiss
from backend.dictionary_api import get_word_data

trie = Trie()
vocabulary = load_vocabulary("datasets/words.txt~")
for word in vocabulary:
    trie.insert(word)

# def intelligent_search(query):

#     if trie.search(query):

#         return {
#             "type": "exact",
#             "result": query
#         }

#     semantic_results = graph.bfs_related_words(query)

#     if semantic_results:

#         return {
#             "type": "graph",
#             "result": semantic_results
#         }

#     embedding_results = semantic_search_faiss(query)

#     if embedding_results:

#         return {
#             "type": "embedding",
#             "result": embedding_results
#         }

#     suggestions = trie.autocomplete(query)

#     if suggestions:

#         return {
#             "type": "autocomplete",
#             "result": suggestions
#         }

#     fuzzy_results = find_closest_words(
#         query,
#         vocabulary
#     )

#     return {
#         "type": "fuzzy",
#         "result": fuzzy_results
#     }

def intelligent_search(query):

    result = {"query": query}

    if trie.search(query):
        result["exact"] = True
    else:
        result["exact"] = False

    result["dictionary"] = simplify_dictionary(
        get_word_data(query)
    )

    result["autocomplete"] = trie.autocomplete(
        query
    )[:5]

    fuzzy_results = find_closest_words(
        query,
        vocabulary
    )[:5]

    result["fuzzy"] = [
        word
        for word, score
        in fuzzy_results
    ]

    graph_results = graph.bfs_related_words_depth(
        query,
        2
    )

    result["graph"] = graph_results[:20]

    semantic_results = semantic_search_faiss(
        query
    )

    result["semantic"] = [
        word
        for word, score
        in semantic_results
    ]

    return result

def simplify_dictionary(data):

    if not data:
        return None

    entry = data[0]

    best_meaning = None

    for meaning in entry["meanings"]:

        if meaning["partOfSpeech"] == "adjective":
            best_meaning = meaning
            break

    if not best_meaning:
        best_meaning = entry["meanings"][0]

    definition = (
        best_meaning["definitions"][0]["definition"]
    )

    synonyms = best_meaning.get(
        "synonyms",
        []
    )[:10]

    antonyms = best_meaning.get(
        "antonyms",
        []
    )[:10]

    return {
        "definition": definition,
        "synonyms": synonyms,
        "antonyms": antonyms
    }

graph = GraphEngine()

# graph.add_edge(
#     "happy",
#     "joyful",
#     0.95
# )

# graph.add_edge(
#     "happy",
#     "cheerful",
#     0.90
# )

# graph.add_edge(
#     "joyful",
#     "excited",
#     0.75
# )

# graph.add_edge(
#     "excited",
#     "energetic",
#     0.60
# )

