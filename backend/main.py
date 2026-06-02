from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.faiss_search import semantic_search_faiss
from backend.search_engine import intelligent_search, trie, graph
from backend.fuzzy_search import find_closest_words, load_vocabulary
from backend.dictionary_api import get_word_data

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load vocabulary
vocabulary = load_vocabulary("datasets/words.txt~")
# HOME ROUTE
@app.get("/")
def home():
    return {
        "message": "Semantic Dictionary AI Backend Running"
    }

# MAIN SEARCH ENGINE
@app.get("/search")
def search(query: str):
    result = intelligent_search(query)
    return result

# AUTOCOMPLETE API
@app.get("/autocomplete")
def autocomplete(prefix: str):
    suggestions = trie.autocomplete(prefix)
    return {
        "suggestions": suggestions
    }

# FUZZY SEARCH API
@app.get("/fuzzy")
def fuzzy(query: str):
    matches = find_closest_words(query, vocabulary)
    return {
        "matches": matches
    }

# GRAPH RELATED WORDS API
@app.get("/graph/related")
def related_words(word: str):
    related = graph.bfs_related_words(word)
    return {
        "related_words": related
    }

# WORD METADATA API
@app.get("/word/{word}")
def word_info(word: str):
    data = get_word_data(word)
    if data:
        return data
    return {
        "error": "Word not found"
    }

# HEALTH CHECK API
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/graph/path")
def graph_path(start: str, end: str):
    path = graph.find_path(start, end)
    return {
        "path": path
    }


@app.get("/graph/depth")
def graph_depth(word: str, depth: int):
    related = graph.bfs_related_words_depth(
        word,
        depth
    )
    return {
        "related_words": related
    }

import time

@app.get("/semantic")
def semantic(query: str):
    start = time.time()
    results = semantic_search_faiss(query)
    print(
        "API Time:",
        time.time() - start
    )
    return {
        "results": results
    }

@app.get(
    "/graph/explore"
)
def explore(
    word: str,
    depth: int = 3
):

    return {
        "results":
        graph.bfs_related_words_depth(
            word,
            depth
        )
    }