from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CommentSerializer
from rest_framework.views import APIView
from .models import Comment


class CommentAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                {"message": "Comment created successfully", "comment_id": comment.id},
                status=201,
            )
        return Response({"errors": serializer.errors}, status=400)

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        print(comments)

        return Response(serializer.data, status=200)
    