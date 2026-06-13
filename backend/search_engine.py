import time

from backend.trie import Trie
from backend.fuzzy_search import find_closest_words, load_vocabulary
from backend.graph_engine import GraphEngine
from backend.faiss_search import semantic_search_faiss
from backend.dictionary_api import get_word_data
from backend.ai_explainer import generate_explanation
import backend.metrics as metrics

# ── startup ───────────────────────────────────────────────────────────────────

trie = Trie()
vocabulary = load_vocabulary("datasets/words.txt~")
for word in vocabulary:
    trie.insert(word)

graph = GraphEngine()


# ── helpers ───────────────────────────────────────────────────────────────────

def _ms(start: float) -> float:
    """Elapsed milliseconds since perf_counter start."""
    return round((time.perf_counter() - start) * 1000, 2)


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

    definition = best_meaning["definitions"][0]["definition"]
    synonyms   = best_meaning.get("synonyms", [])[:10]
    antonyms   = best_meaning.get("antonyms", [])[:10]

    return {
        "definition": definition,
        "synonyms":   synonyms,
        "antonyms":   antonyms,
    }


def build_graph_visualization(query):
    nodes = [{"id": query}]
    edges = []

    if query not in graph.graph:
        return {"nodes": nodes, "edges": edges}

    for neighbor, weight in graph.graph[query]:
        nodes.append({"id": neighbor})
        edges.append({
            "source": query,
            "target": neighbor,
            "weight": round(weight, 2),
        })

    return {"nodes": nodes, "edges": edges}


# ── main pipeline ─────────────────────────────────────────────────────────────

def intelligent_search(query: str) -> dict:
    result = {"query": query}

    # 1. Trie exact lookup
    t = time.perf_counter()
    result["exact"] = trie.search(query)
    metrics.last_latency["trie_lookup_ms"] = _ms(t)

    # 2. Dictionary API (live HTTP call)
    t = time.perf_counter()
    result["dictionary"] = simplify_dictionary(get_word_data(query))
    metrics.last_latency["dict_api_ms"] = _ms(t)

    # 3. Trie autocomplete
    t = time.perf_counter()
    result["autocomplete"] = trie.autocomplete(query)[:5]
    metrics.last_latency["autocomplete_ms"] = _ms(t)

    # 4. Levenshtein fuzzy correction (brute-force O(N·L²))
    t = time.perf_counter()
    fuzzy_results = find_closest_words(query, vocabulary)[:5]
    result["fuzzy"] = [word for word, _ in fuzzy_results]
    metrics.last_latency["fuzzy_search_ms"] = _ms(t)

    # 5. Graph BFS
    t = time.perf_counter()
    graph_results = graph.bfs_related_words_depth(query, 2)
    result["graph"] = graph_results[:20]
    metrics.last_latency["graph_bfs_ms"] = _ms(t)

    # 6. Graph visualization (BFS already done, just formatting)
    result["graph_visualization"] = graph.get_visualization_data(query, 2)

    # 7. FAISS semantic search
    t = time.perf_counter()
    semantic_results = semantic_search_faiss(query)
    result["semantic"] = [word for word, _ in semantic_results]
    metrics.last_latency["faiss_search_ms"] = _ms(t)

    # 8. Gemini AI explanation
    t = time.perf_counter()
    definition = result["dictionary"]["definition"] if result["dictionary"] else ""
    result["ai_explanation"] = generate_explanation(
        query,
        definition,
        result["semantic"][:5],
        result["graph"][:10],
    )
    metrics.last_latency["gemini_ms"] = _ms(t)

    return result