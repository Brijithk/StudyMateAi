from documents.models import Document
from documents.services.pdf_processor import (
    extract_text_from_pdf,
    chunk_text,
)
from documents.services.vector_store import store_chunks


def process_document(document_id):
    """
    Extract, chunk, and index a PDF document.
    Update its status based on the processing result.
    """

    document = Document.objects.get(id=document_id)

    try:
        document.status = "processing"
        document.save(update_fields=["status"])

        # 1. Extract text from the PDF.
        pages = extract_text_from_pdf(document.file.path)

        if not pages:
            raise ValueError(
                "No extractable text found in this PDF."
            )

        # 2. Split each page into chunks.
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

        if not all_chunks:
            raise ValueError(
                "No text chunks were generated."
            )

        # 3. Store the chunks and their embeddings.
        stored_count = store_chunks(all_chunks)

        if stored_count != len(all_chunks):
            raise RuntimeError(
                "Not all document chunks were stored."
            )

        # 4. Mark the document as completed.
        document.status = "completed"
        document.save(update_fields=["status"])

        return {
            "document_id": document.id,
            "status": document.status,
            "pages_processed": len(pages),
            "chunks_stored": stored_count,
        }

    except Exception:
        document.status = "failed"
        document.save(update_fields=["status"])
        raise