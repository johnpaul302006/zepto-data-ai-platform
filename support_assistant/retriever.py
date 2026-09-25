from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"


# Load the same embedding model used during indexing
model = SentenceTransformer(MODEL_NAME)

# Connect to the persistent ChromaDB database
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Load the existing policy collection
collection = client.get_collection(name="zepto_policies")


def retrieve_documents(query: str, top_k: int = 3) -> list[dict]:
    """
    Retrieve the most similar Zepto policy documents.

    ChromaDB is configured to use cosine distance.
    """

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )

    retrieved_documents = []

    documents = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        retrieved_documents.append(
            {
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_documents


if __name__ == "__main__":
    query = "How long does Zepto delivery take?"

    print(f"Query: {query}")
    print("\nTop retrieved documents:\n")

    results = retrieve_documents(query, top_k=3)

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['id']}")
        print(f"   Distance: {result['distance']}")
        print(f"   Source: {result['metadata']['source']}")
        print(f"   Text: {result['document'][:200]}...")
        print()