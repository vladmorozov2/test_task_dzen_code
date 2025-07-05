from .views import UserAPIView

from django.urls import path

urlpatterns = [
    path("user/", UserAPIView.as_view(), name="user_api"),
]
