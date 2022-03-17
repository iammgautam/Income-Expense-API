import imp
from django.urls import path
from authentication.views import RegistraterViews

urlpatterns = [
    path('register/', RegistraterViews.as_view(), name='register'),
]
