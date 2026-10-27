import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from documents.models import Document
from documents.services.pdf_processor import (
    extract_text_from_pdf,
    chunk_text,
)
from documents.services.vector_store import (
    store_chunks,
    search_chunks,
)


# Get the previously uploaded PDF.
document = Document.objects.get(id=1)

# Extract text page by page.
pages = extract_text_from_pdf(document.file.path)

# Create chunks with page metadata.
all_chunks = []

for page in pages:
    page_chunks = chunk_text(page["text"])

    for index, chunk in enumerate(page_chunks):
        all_chunks.append({
            "document_id": document.id,
            "page_number": page["page_number"],
            "chunk_index": index,
            "text": chunk,
        })

print("Document:", document.title)
print("Chunks generated:", len(all_chunks))

# Store chunks and embeddings.
stored_count = store_chunks(all_chunks)

print("Chunks stored in ChromaDB:", stored_count)

# Search for relevant Python notes.
question = "How do I define and use a function in Python?"

results = search_chunks(
    query=question,
    document_id=document.id,
    top_k=5
)

print("\nQuestion:", question)
print("\nRelevant results:")

for index, result in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print("Page:", result["metadata"]["page_number"])
    print("Distance:", round(result["distance"], 4))
    print(result["text"][:500])