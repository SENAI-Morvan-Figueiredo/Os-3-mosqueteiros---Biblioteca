from django.urls import path
from .views import register

urlpatterns = [
    path('cadastro/', register, name='user_register'),
]