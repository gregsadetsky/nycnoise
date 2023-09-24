from django.contrib import admin
from django.urls import include, path

from .views import index

urlpatterns = [
    path("", index),
]
