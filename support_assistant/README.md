# Zepto Support Assistant

## Overview

The Zepto Support Assistant is a Retrieval-Augmented Generation (RAG)
service that answers questions about Zepto policies using a local
document corpus, local embeddings, ChromaDB, LangGraph, Pydantic, and
FastAPI.

The graded configuration uses offline mock mode by default. This means
the required workflow does not need an external LLM API key.

---

## RAG Architecture

The complete RAG pipeline is:

```text
Zepto Policy Documents
        |
        v
Ingestion and Chunking
        |
        |  ingest.py
        v
Embedding
all-MiniLM-L6-v2
        |
        v
ChromaDB
zepto_policies
        |
        |
User Query
        |
        v
LangGraph
classify_intent
        |
        +--------------------------+
        |                          |
        v                          v
policy_question            general_question
        |                          |
        v                          v
retrieve_and_answer          direct_answer
        |
        v
Top-3 ChromaDB Retrieval
        |
        v
Mock/LLM Generation
        |
        +--------------------------+
                                   |
                                   v
                         Pydantic Response
                     answer / sources / confidence
                                   |
                                   v
                              FastAPI
                             POST /ask