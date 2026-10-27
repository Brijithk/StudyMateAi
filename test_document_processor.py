import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from documents.services.document_processor import process_document

result = process_document(1)

print("\nDocument processing successful!")
print("Document ID:", result["document_id"])
print("Status:", result["status"])
print("Pages processed:", result["pages_processed"])
print("Chunks stored:", result["chunks_stored"])