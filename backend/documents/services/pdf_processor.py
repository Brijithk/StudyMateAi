import fitz


def extract_text_from_pdf(file_path):
    """
    Extract text from every page of a PDF.
    """

    extracted_pages = []

    with fitz.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")

            if page_text.strip():
                extracted_pages.append({
                    "page_number": page_number,
                    "text": page_text.strip()
                })

    return extracted_pages