from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .serializers import CommentSerializer
from .models import Comment
import math


class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

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
            return Response(
                {"message": "Comment created successfully", "comment_id": comment.id},
                status=201,
            )
        return Response({"errors": serializer.errors}, status=400)

    def get(self, request):
        queryset = Comment.objects.all().order_by("-created_at")
        user_id = request.user.id if request.user.is_authenticated else None
        print("User ID:", user_id)
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get("per_page", 25))
        page = paginator.paginate_queryset(queryset, request)

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
