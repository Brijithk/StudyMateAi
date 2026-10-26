import os
import sys
import django

# Add the backend folder to Python's import path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)

# Configure Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from documents.models import Document
from documents.services.pdf_processor import extract_text_from_pdf


# Retrieve the uploaded PDF
document = Document.objects.get(id=1)

# Get the actual file path
pdf_path = document.file.path

# Extract text
pages = extract_text_from_pdf(pdf_path)

print("Document:", document.title)
print("Pages containing text:", len(pages))

for page in pages[:2]:
    print(f"\n--- Page {page['page_number']} ---")
    print(page["text"][:1000])