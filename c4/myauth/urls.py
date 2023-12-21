from django.urls import path
from .views import *

urlpatterns = [
    path('register/', ProfileRegisterView.as_view()),
    path('otp-create/', OtpCreateView.as_view()),
    path('otp-check/', OtpCheckView.as_view()),
]