from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id if request.user.is_authenticated else None
        print("User ID:", user_id, flush=True)
        print("Headers:", request.headers, flush=True)
        user = User.objects.all().filter(id=user_id).first()
        serializer = UserSerializer(
            user,
        )
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully", "user_id": user.id},
                status=201,
            )
        return Response({"errors": serializer.errors}, status=400)
