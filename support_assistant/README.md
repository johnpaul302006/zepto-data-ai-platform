# Zepto Support Assistant

## Overview

The Zepto Support Assistant is a policy-focused Retrieval-Augmented Generation (RAG) service.

The graded baseline uses deterministic offline `MOCK_LLM` mode, so no external LLM API key is required.

Technologies used:

- Python
- Sentence Transformers
- ChromaDB
- LangGraph
- Pydantic
- FastAPI
- Uvicorn
- Docker

## RAG Architecture

```text
Zepto Policy Documents
        |
        v
ingest.py
Read documents and create chunks
        |
        v
all-MiniLM-L6-v2
Generate embeddings
        |
        v
ChromaDB
Store embeddings and documents
        |
        v
User Query
        |
        v
graph.py
classify_intent
        |
        +-----------------------------+
        |                             |
        v                             v
policy_question                 general_question
        |                             |
        v                             v
retrieve_and_answer              direct_answer
        |
        v
retriever.py
Top-3 cosine-similarity retrieval
        |
        v
Mock / Optional LLM generation
        |
        v
Pydantic SupportResponse
        |
        v
FastAPI POST /ask