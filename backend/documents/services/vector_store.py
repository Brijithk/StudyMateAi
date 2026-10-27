import chromadb
from sentence_transformers import SentenceTransformer


# Persistent storage for ChromaDB
CHROMA_DB_PATH = "chroma_db"

# Load the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Create or retrieve the collection
collection = client.get_or_create_collection(
    name="study_documents",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks(chunks):
    """
    Generate embeddings and store document chunks in ChromaDB.
    """

    if not chunks:
        return 0

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()

    ids = [
        (
            f"doc_{chunk['document_id']}"
            f"_page_{chunk['page_number']}"
            f"_chunk_{chunk['chunk_index']}"
        )
        for chunk in chunks
    ]

    metadatas = [
        {
            "document_id": chunk["document_id"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    # Upsert inserts new chunks or updates existing IDs.
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def search_chunks(query, document_id, top_k=5):
    """
    Find the most relevant chunks for a question
    within a specific document.
    """

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20.")

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, max(1, collection.count())),
        where={"document_id": document_id},
        include=["documents", "metadatas", "distances"]
    )

    matches = []

    for index, text in enumerate(results["documents"][0]):
        matches.append({
            "text": text,
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return matches