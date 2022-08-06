from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from user import views

urlpatterns = [
    path("sign-up", views.SignUpView.as_view(), name="sign-up"),
    path("sign-in", TokenObtainPairView.as_view(), name="sign-in"),
]
