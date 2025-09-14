from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('resend', views.ResendOTP.as_view(), name='resendotp'),
    path('verify', views.VerifyEmailView.as_view(), name='verify_email'),
    path('login', views.LoginView.as_view(), name='login'),
    path('post', views.postview.as_view(), name='post'),
    path('broadcast', views.UserPostsView.as_view(), name='broadcast-post'),
]
