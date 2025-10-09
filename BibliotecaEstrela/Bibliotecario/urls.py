from django.urls import path
from .views import *
app_name = 'Bibliotecario'
urlpatterns = [
    path("", teste, name="teste"),
]