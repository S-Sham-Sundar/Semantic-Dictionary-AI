# Semantic Dictionary AI Architecture

## Entry Point

main.py

Browser
↓
main.py
↓
search_engine.py

---

## Search Components

search_engine.py

Uses:

- trie.py
- fuzzy_search.py
- dictionary_api.py
- graph_engine.py
- faiss_search.py

---

## Semantic Search Pipeline

Query
↓
Sentence Transformer
↓
Embedding Vector
↓
FAISS
↓
Top Semantic Matches

Files:

- embedding_store.py
- vector_index.py
- faiss_search.py

---

## Graph Pipeline

FAISS
↓
semantic_graph_builder.py
↓
semantic_graph.pkl
↓
graph_engine.py

---

## Active Files

- main.py
- search_engine.py
- trie.py
- fuzzy_search.py
- dictionary_api.py
- graph_engine.py
- faiss_search.py

---

## Experimental Files

- semantic_graph_builder.py
- semantic_graph_loader.py

---

## Legacy Files

- embedding_search.py (brute force search)