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

document = Document.objects.get(id=1)

pages = extract_text_from_pdf(document.file.path)

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
print("Pages containing text:", len(pages))
print("Total chunks:", len(all_chunks))

if all_chunks:
    print("\n--- First Chunk ---")
    print(all_chunks[0]["text"])

    print("\n--- First Chunk Metadata ---")
    print({
        "document_id": all_chunks[0]["document_id"],
        "page_number": all_chunks[0]["page_number"],
        "chunk_index": all_chunks[0]["chunk_index"],
    })