import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .serializers import CommentSerializer
from .models import Comment
import math

# Put your secret key here (get it from Google reCAPTCHA admin console)
RECAPTCHA_SECRET_KEY = "6LfpsHkrAAAAAHX_2JsEynL0hgnMOwKkoaIYslzH"

class CommentAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def verify_captcha(self, token, remote_ip=None):
        """Verify captcha token with Google"""
        url = "https://www.google.com/recaptcha/api/siteverify"
        data = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token,
        }
        if remote_ip:
            data['remoteip'] = remote_ip

        try:
            r = requests.post(url, data=data)
            result = r.json()
            return result.get("success", False)
        except Exception as e:
            # Log the exception if needed
            return False

    def post(self, request):
        captcha_token = request.data.get('captcha')
        if not captcha_token:
            return Response({"error": "Captcha token is required."}, status=400)

        user_ip = request.META.get('REMOTE_ADDR')
        if not self.verify_captcha(captcha_token, user_ip):
            return Response({"error": "Captcha verification failed."}, status=400)

        data = request.data.copy()
        user = request.user

        data["sender"] = user.id
        data["username"] = user.username
        data["email"] = user.email
        data['homepage'] = getattr(user, 'homepage', '')  # safe access

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            comment = serializer.save()
            # Clear cache after creating a new comment so GET gets fresh data
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
