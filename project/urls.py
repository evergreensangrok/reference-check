from django.contrib import admin
from django.urls import include, path

from project import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping", views.PingView.as_view()),
    path("user/", include("user.urls")),
    path("reference/", include("reference.urls")),
]
