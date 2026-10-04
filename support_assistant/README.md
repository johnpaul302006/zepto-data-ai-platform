# Zepto Support Assistant

## Overview

The Zepto Support Assistant is a policy-focused Retrieval-Augmented Generation (RAG) service.

It uses:

- Local policy documents
- `all-MiniLM-L6-v2` for embeddings
- ChromaDB for vector storage
- LangGraph for workflow orchestration
- Pydantic for structured responses
- FastAPI for the API

The graded configuration uses deterministic offline mock mode by default, so no external LLM API key is required.

---

## Architecture

```text
Zepto Policy Documents
        |
        v
Ingestion and Chunking
        |
        v
Local Embeddings
all-MiniLM-L6-v2
        |
        v
ChromaDB
        |
        v
User Query
        |
        v
LangGraph
        |
        +-----------------------+
        |                       |
        v                       v
classify_intent          general_question
        |                       |
        v                       v
policy_question          direct_answer
        |
        v
retrieve_and_answer
        |
        v
Top-3 Retrieval
        |
        v
Mock/Optional LLM
        |
        v
Pydantic Validation
        |
        v
FastAPI POST /ask