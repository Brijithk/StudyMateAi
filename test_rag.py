import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from documents.models import Document
from documents.services.rag_service import answer_question


document = Document.objects.get(id=1)

question = "How do I define and use a function in Python?"

result = answer_question(
    question=question,
    document_id=document.id,
)

print("\nQuestion:")
print(question)

print("\nStudyMate AI Answer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(
        f"Page {source['page_number']} "
        f"(distance: {source['distance']})"
    )