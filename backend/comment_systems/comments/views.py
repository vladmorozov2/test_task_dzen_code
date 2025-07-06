from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .serializers import CommentSerializer
from .models import Comment
import math


class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data.copy()
        user = request.user

        data["sender"] = user.id
        data["username"] = user.username
        data["email"] = user.email
        data['homepage'] = user.homepage
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            # Очищаємо кеш після створення нового коментаря,
            # щоб get отримував оновлені дані
            cache.clear()
            return Response(
                {"message": "Comment created successfully", "comment_id": comment.id},
                status=201,
            )
        return Response({"errors": serializer.errors}, status=400)

    def get(self, request):
        page_num = request.query_params.get("page", "1")
        per_page = int(request.query_params.get("per_page", 25))

        cache_key = f"comments_page_{page_num}_per_{per_page}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)

        queryset = Comment.objects.all().order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = per_page
        page = paginator.paginate_queryset(queryset, request)

        total = queryset.count()
        last_page = math.ceil(total / per_page)
        current_page = int(page_num)

        serializer = CommentSerializer(page, many=True)

        response_data = {
            "data": serializer.data,
            "meta": {
                "total": total,
                "per_page": per_page,
                "current_page": current_page,
                "last_page": last_page,
            },
        }

        cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)
