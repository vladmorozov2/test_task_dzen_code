from .views import CommentAPIView
from django.urls import path

urlpatterns = [
    path("comments/", CommentAPIView.as_view(), name="comment"),
]
