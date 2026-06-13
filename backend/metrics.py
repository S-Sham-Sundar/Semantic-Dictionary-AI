"""
metrics.py — pipeline latency store

Written to by search_engine.py on every /search call.
Read by the GET /metrics endpoint in main.py.

All values are in milliseconds (float).
None = stage not yet executed since server start.
"""

from typing import Dict, Optional

last_latency: Dict[str, Optional[float]] = {
    "trie_lookup_ms":        None,
    "dict_api_ms":           None,
    "autocomplete_ms":       None,
    "fuzzy_search_ms":       None,
    "graph_bfs_ms":          None,
    "graph_visualization_ms": None,
    "faiss_search_ms":       None,
    "gemini_ms":             None,
}