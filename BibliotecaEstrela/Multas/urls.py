from django.urls import path
from .views import mp_webhook

urlpatterns = [
    path("webhook/", mp_webhook, name="mp_webhook"),
]