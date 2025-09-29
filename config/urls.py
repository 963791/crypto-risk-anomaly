from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Example: point to your apps
    # path("api/", include("apps.your_app.urls")),
]
