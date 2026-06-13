from dotenv import load_dotenv
load_dotenv()

import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.faiss_search import semantic_search_faiss
from backend.search_engine import intelligent_search, trie, graph
from backend.fuzzy_search import find_closest_words, load_vocabulary
from backend.dictionary_api import get_word_data
import backend.metrics as metrics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500",
                   "http://localhost:3000", "null"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

vocabulary = load_vocabulary("datasets/words.txt~")

# ── existing routes (all preserved) ──────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Semantic Dictionary AI Backend Running"}


@app.get("/search")
def search(query: str):
    return intelligent_search(query)


@app.get("/autocomplete")
def autocomplete(prefix: str):
    return {"suggestions": trie.autocomplete(prefix)}


@app.get("/fuzzy")
def fuzzy(query: str):
    return {"matches": find_closest_words(query, vocabulary)}


@app.get("/graph/related")
def related_words(word: str):
    return {"related_words": graph.bfs_related_words(word)}


@app.get("/word/{word}")
def word_info(word: str):
    data = get_word_data(word)
    return data if data else {"error": "Word not found"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/graph/path")
def graph_path(start: str, end: str):
    return {"path": graph.find_path(start, end)}


@app.get("/graph/depth")
def graph_depth(word: str, depth: int):
    return {"related_words": graph.bfs_related_words_depth(word, depth)}


@app.get("/semantic")
def semantic(query: str):
    start = time.time()
    results = semantic_search_faiss(query)
    print("API Time:", time.time() - start)
    return {"results": results}


@app.get("/graph/explore")
def explore(word: str, depth: int = 3):
    return {"results": graph.bfs_related_words_depth(word, depth)}


# ── NEW: metrics endpoint ─────────────────────────────────────────────────────

@app.get("/metrics")
def get_metrics():
    """
    Returns the measured latency (ms) of each pipeline stage
    from the most recent /search call.
    Values are null until /search has been called at least once.

    Example response:
    {
        "trie_lookup_ms":         0.08,
        "dict_api_ms":          143.52,
        "autocomplete_ms":        0.12,
        "fuzzy_search_ms":       21.84,
        "graph_bfs_ms":           1.42,
        "graph_visualization_ms": 0.31,
        "faiss_search_ms":        4.31,
        "gemini_ms":            682.54
    }
    """
    return metrics.last_latency