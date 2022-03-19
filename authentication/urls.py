from django.urls import path
from authentication.views import LoginAPIView, RegistraterViews, VerifyEmail

urlpatterns = [
    path('register/', RegistraterViews.as_view(), name='register'),
     path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]

