from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('resend', views.ResendOTP.as_view(), name='resendotp'),
    path('verify', views.VerifyEmailView.as_view(), name='verify_email'),
    path('login', views.LoginView.as_view(), name='login'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('post', views.postview.as_view(), name='post'),
    path('broadcast', views.UserPostsView.as_view(), name='broadcast-post'),
    path('password_reset/request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/confirm/<uuid:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
