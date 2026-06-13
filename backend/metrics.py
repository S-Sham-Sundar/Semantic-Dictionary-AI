"""
metrics.py — lightweight latency store

Holds the timing (in milliseconds) of the most recent execution of each
pipeline stage. Written to by search_engine.py, read by the /metrics route.

Not thread-safe for high concurrency, but perfectly fine for a single-process
demo server — last write wins, which is all we need.
"""

from typing import Dict, Optional

# Filled in by search_engine.py on every /search call
last_latency = {
    "trie_lookup_ms":           None,
    "dict_api_ms":              None,
    "autocomplete_ms":          None,
    "fuzzy_search_ms":          None,
    "graph_bfs_ms":             None,
    "graph_visualization_ms":   None,   
    "faiss_search_ms":          None,
    "gemini_ms":                None,
}

# Filled in by the /ai/explain route
last_explain_latency: Dict[str, Optional[float]] = {
    "redis_get_ms":   None,
    "ollama_ms":      None,
    "redis_set_ms":   None,
}