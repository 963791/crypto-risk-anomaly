from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path("", views.HealthView.as_view(), name="accounts-health"),
]

