from django.contrib import admin
from django.urls import path
from api.views import index, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register', register),
]
