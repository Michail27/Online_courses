from django.contrib import admin
from django.urls import path, include

from clases.views import Register

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
]