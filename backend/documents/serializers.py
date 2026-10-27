from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document

        fields = [
            'id',
            'title',
            'file',
            'status',
            'uploaded_at',
        ]

        read_only_fields = [
            'id',
            'status',
            'uploaded_at',
        ]

class AskQuestionSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(min_value=1)
    question = serializers.CharField(
        max_length=2000,
        trim_whitespace=True
    )