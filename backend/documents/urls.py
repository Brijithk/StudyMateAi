from django.urls import path

from .views import (
    DocumentUploadView,
    AskQuestionView,
    DocumentListView,
)

urlpatterns = [
    path(
        "",
        DocumentListView.as_view(),
        name="document-list",
    ),
    path(
        "upload/",
        DocumentUploadView.as_view(),
        name="document-upload",
    ),
    path(
        "ask/",
        AskQuestionView.as_view(),
        name="ask-question",
    ),
]