from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CommentSerializer
from rest_framework.views import APIView
from .models import Comment
import math
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class CommentAPIView(APIView):
    def post(self, request):
        # Combine data and files
        data = request.data.copy()

        # Handle attachment from files
        if "attachment" in request.FILES:
            data["attachment"] = request.FILES["attachment"]

        serializer = CommentSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            try:
                comment = serializer.save()
                # Serialize again to include read-only fields
                response_serializer = CommentSerializer(
                    comment, context={"request": request}
                )
                return Response(
                    {
                        "message": "Comment created successfully",
                        "comment": response_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        queryset = Comment.objects.all().order_by("-created_at")

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get("per_page", 25))
        page = paginator.paginate_queryset(queryset, request)

        # Total count
        total = queryset.count()
        per_page = paginator.page_size
        last_page = math.ceil(total / per_page)
        current_page = int(request.query_params.get("page", 1))

        serializer = CommentSerializer(page, many=True, context={"request": request})

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
