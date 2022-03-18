import imp
from django.urls import path
from authentication.views import RegistraterViews, VerifyEmail

urlpatterns = [
    path('register/', RegistraterViews.as_view(), name='register'),
    path('email-verify/',VerifyEmail.as_view(), name='email-verify'),
]
