from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CommentSerializer
from rest_framework.views import APIView
from .models import Comment
import math
from rest_framework.pagination import PageNumberPagination

class CommentAPIView(APIView):
    def post(self, request):
        data = request.data
        print("Received data:", data)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                {"message": "Comment created successfully", "comment_id": comment.id},
                status=201,
            )
        return Response({"errors": serializer.errors}, status=400)

    def get(self, request):
        queryset = Comment.objects.all().order_by("-created_at")

        # Пагінація
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get("per_page", 1))
        page = paginator.paginate_queryset(queryset, request)

        # Загальна кількість
        total = queryset.count()
        per_page = paginator.page_size
        last_page = math.ceil(total / per_page)
        current_page = int(request.query_params.get("page", 1))

        serializer = CommentSerializer(page, many=True)

        return Response(
            {
                "data": serializer.data,
                "meta": {
                    "total": total,
                    "per_page": per_page,
                    "current_page": current_page,
                    "last_page": last_page,
                },
            }
        )
