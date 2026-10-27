import pymupdf


def extract_text_from_pdf(file_path):
    """
    Extract text from every page of a PDF.
    """

    extracted_pages = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")

            if page_text.strip():
                extracted_pages.append({
                    "page_number": page_number,
                    "text": page_text.strip()
                })

    return extracted_pages


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.

    chunk_size: Maximum number of characters per chunk.
    overlap: Number of characters shared between consecutive chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and less than chunk_size.")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks