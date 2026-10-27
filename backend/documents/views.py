from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer, AskQuestionSerializer
from .services.document_processor import process_document
from .services.rag_service import answer_question
import logging

logger = logging.getLogger(__name__)

class DocumentUploadView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

def perform_create(self, serializer):
    document = serializer.save(user=self.request.user)

    try:
        process_document(document.id)
    except Exception:
        logger.exception(
            "Failed to process uploaded document %s",
            document.id,
        )

    document.refresh_from_db()
    document.refresh_from_db()

class AskQuestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AskQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document_id = serializer.validated_data["document_id"]
        question = serializer.validated_data["question"]

        document = Document.objects.filter(
            id=document_id,
            user=request.user,
        ).first()

        if document is None:
            return Response(
                {"error": "Document not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if document.status != "completed":
            return Response(
                {
                    "error": (
                        "This document is not ready for questions yet."
                    ),
                    "document_status": document.status,
                },
                status=status.HTTP_409_CONFLICT,
            )

        try:
            result = answer_question(
                question=question,
                document_id=document.id,
            )

            return Response(
                {
                    "document_id": document.id,
                    "question": question,
                    "answer": result["answer"],
                    "sources": result["sources"],
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            return Response(
                {
                    "error": (
                        "Unable to generate an answer right now. "
                        "Please try again later."
                    )
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            user=self.request.user
        ).order_by("-uploaded_at")