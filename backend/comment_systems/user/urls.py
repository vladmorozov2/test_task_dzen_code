from .views import UserAPIView

from django.urls import path

urlpatterns = [
    path("register/", UserAPIView.as_view(), name="user-register"),
]
