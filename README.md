# Semantic Dictionary AI

A dictionary and semantic search engine built in Python. Combines classical data structures with an AI retrieval layer — all exposed through a FastAPI backend and a vanilla JS frontend.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Benchmarks](#benchmarks)
- [AI Explanation Layer](#ai-explanation-layer)
- [API Reference](#api-reference)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)
- [Future Work](#future-work)

---

## Overview

Traditional dictionary lookup only works if you spell the word correctly and already know the word you want. It can't answer "what's the word for feeling happy at someone else's misfortune" or correct "meloncolly" into "melancholy."

This project solves that by layering three kinds of search on top of a 99K-word vocabulary: exact/fuzzy character matching, graph traversal over word relationships, and embedding-based semantic retrieval. A single query runs through all three layers and returns one unified result.

---

## Features

- Exact word lookup via a Trie (O(L))
- Prefix autocomplete (DFS from the prefix node)
- Levenshtein fuzzy correction for misspelled queries
- Semantic graph traversal (BFS) over FAISS-derived word neighbours
- FAISS vector search over SentenceTransformer embeddings
- Live dictionary definitions, synonyms, antonyms
- Gemini-generated plain-English explanations
- Per-stage latency instrumentation (`/metrics`)

---

## Architecture

```
Browser (index.html + script.js)
        │  GET /search?query=
        ▼
FastAPI (main.py)
        ▼
intelligent_search()  (search_engine.py)
        ├── Trie.search()            trie.py
        ├── get_word_data()          dictionary_api.py    → dictionaryapi.dev
        ├── Trie.autocomplete()      trie.py
        ├── find_closest_words()     fuzzy_search.py       (Levenshtein)
        ├── GraphEngine.bfs_*()      graph_engine.py        → semantic_graph.pkl
        ├── semantic_search_faiss()  faiss_search.py        → embedding_cache.pkl
        └── generate_explanation()   ai_explainer.py         → Gemini 2.5 Flash
```

Offline build (run once before the server starts):

```
words.txt~ ──> embedding_store.py ──> embedding_cache.pkl ──┐
                                                            ├─> faiss_search.py
embedding_cache.pkl ──> semantic_graph_builder.py ──> semantic_graph.pkl ──> graph_engine.py
```

---

## Tech Stack

- **Python** — FastAPI, NumPy, Requests
- **SentenceTransformers** — `all-MiniLM-L6-v2` (384-dim embeddings)
- **FAISS** — `IndexFlatIP` for vector similarity search
- **Gemini 2.5 Flash** — AI explanation generation
- **Vanilla JS / HTML / CSS** — frontend, no framework

---

## Benchmarks

Every pipeline stage is timed independently with `time.perf_counter()`. Real measured output from `/metrics`:

```json
{
  "trie_lookup_ms":          0.08,
  "dict_api_ms":           143.52,
  "autocomplete_ms":         0.12,
  "fuzzy_search_ms":        21.84,
  "graph_bfs_ms":            1.42,
  "graph_visualization_ms":  0.31,
  "faiss_search_ms":         4.31,
  "gemini_ms":             682.54
}
```

The DSA layers (Trie, BFS, FAISS) are all sub-5ms. The two external API calls — Dictionary and Gemini — dominate total latency.

---

## AI Explanation Layer

After all retrieval layers run, the query word, its definition, FAISS semantic neighbours, and BFS graph neighbours are passed to Gemini 2.5 Flash, which generates a short, grounded, plain-English explanation. This is a lightweight RAG pattern — retrieval happens first, generation is constrained to that retrieved context rather than answering from the model's own knowledge alone.

---

## API Reference

| Endpoint | Purpose |
|---|---|
| `GET /search?query=` | Full pipeline — returns all results in one response |
| `GET /autocomplete?prefix=` | Trie prefix completions |
| `GET /fuzzy?query=` | Levenshtein closest matches |
| `GET /semantic?query=` | FAISS nearest neighbours |
| `GET /graph/related?word=` | BFS related words |
| `GET /graph/path?start=&end=` | Shortest path between two words |
| `GET /metrics` | Per-stage latency from the last search (ms) |
| `GET /health` | Health check |

---

## Setup

```bash
git clone https://github.com/S-Sham-Sundar/Semantic-Dictionary-AI.git
cd Semantic-Dictionary-AI
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Add your Gemini API key to a `.env` file:
```
GEMINI_API_KEY=your-key-here
```

Build the offline artifacts (run once):
```bash
python backend/ai_pipeline/embedding_store.py
python backend/graph_pipeline/semantic_graph_builder.py
```

Start the server:
```bash
uvicorn backend.main:app --reload
```

Open `frontend/index.html` in a browser.

---

## Project Structure

```
backend/
  main.py              FastAPI routes
  search_engine.py     Unified pipeline with per-stage latency timing
  trie.py              Trie — insert, search, autocomplete
  fuzzy_search.py      Levenshtein edit distance
  graph_engine.py      BFS traversal and path finding
  faiss_search.py      FAISS semantic search
  dictionary_api.py    dictionaryapi.dev client
  ai_explainer.py      Gemini explanation generation
  cache_service.py     Redis cache wrapper
  metrics.py           Latency store — written per search, read by /metrics
  ai_pipeline/         Offline embedding scripts
  graph_pipeline/      Offline graph builder scripts

frontend/
  index.html
  script.js
  style.css

datasets/
  words.txt~           99K word vocabulary
```

---

## Design Decisions

**Why Trie + Levenshtein instead of just a database query?** A database index handles exact lookup fine, but neither autocomplete nor typo tolerance come for free from SQL. The Trie gives O(L) prefix search; Levenshtein DP gives edit-distance correction. Both are implemented from scratch rather than via a library, to demonstrate the underlying algorithm.

**Why FAISS over a managed vector database?** FAISS runs in-process with no external service, which keeps the project simple to set up and run locally. `IndexFlatIP` does exact search rather than approximate — acceptable at 99K vectors, and avoids the accuracy tradeoffs of ANN indexes for a project at this scale.

**Why is the similarity graph built from FAISS neighbours instead of WordNet?** It reuses the same embedding space already built for semantic search, so no second data source or licensing dependency is needed. The tradeoff is honest: it's an embedding-derived graph, not a lexicographic one — edges reflect learned similarity, not curated synonym relationships.

**Why is Gemini called last, not first?** All retrieval (Trie, fuzzy, FAISS, graph, dictionary) runs before the LLM call, and only the retrieved results are passed into the prompt. This grounds the explanation in real retrieved data rather than letting Gemini answer purely from its own training.

---

## Future Work

- Redis caching for Gemini explanations (7-day TTL) — cuts repeat-query latency from ~700ms to <1ms
- BK-Tree for fuzzy search — replaces O(N·L²) brute-force Levenshtein with O(log N) average lookup
- Frequency-ranked autocomplete — rank Trie completions by usage instead of returning them unordered
- Local SQLite store for definitions — removes the live external API call from the hot path
- Docker packaging for one-command setup
