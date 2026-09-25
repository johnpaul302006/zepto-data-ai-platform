from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CORPUS_DIR = BASE_DIR / "corpus"
CHROMA_DIR = BASE_DIR / "chroma_db"


# ---------------------------------------------------------
# Load embedding model
# ---------------------------------------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------------
# Read all corpus documents
# ---------------------------------------------------------
documents = []
document_ids = []
metadatas = []

for file_path in sorted(CORPUS_DIR.glob("*.txt")):
    text = file_path.read_text(encoding="utf-8").strip()

    if not text:
        continue

    documents.append(text)
    document_ids.append(file_path.stem)
    metadatas.append({"source": file_path.name})


print(f"Documents loaded: {len(documents)}")


# ---------------------------------------------------------
# Generate embeddings
# ---------------------------------------------------------
print("Generating embeddings...")

embeddings = model.encode(
    documents,
    normalize_embeddings=True,
    show_progress_bar=True,
).tolist()


# ---------------------------------------------------------
# Create ChromaDB client and collection
# ---------------------------------------------------------
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="zepto_policies",
    configuration={
        "hnsw": {
            "space": "cosine",
        }
    },
)


# ---------------------------------------------------------
# Store documents + embeddings
# ---------------------------------------------------------
collection.upsert(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas,
)


# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------
print(f"Documents stored in ChromaDB: {collection.count()}")
print(f"ChromaDB location: {CHROMA_DIR}")

print("\nIndexed document IDs:")
for doc_id in document_ids:
    print(f" - {doc_id}")

print("\nEmbedding and ChromaDB indexing completed successfully.")