from django.contrib import admin
from django.urls import path

from project import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping", views.PingView.as_view()),
]
