from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
import re
from django.conf import settings

from .models import CustomUser, EmailVerificationCode, postmodel
from .serializers import (
    RegisterSerializer, VerifyEmailSerializer,
    LoginSerializer, CustomUserSerializer, postserializer
)
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp = EmailVerificationCode.generate_code()
            EmailVerificationCode.objects.create(user=user, otp=otp)

            send_mail(
                "Your verification code",
                f"Use this code to verify your account: {otp}",
                "belloabdulrahmon345@gmail.com",
                [user.email],
            )

            return Response({"message": "User registered. Verification code sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ResendOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return Response(
                {"message": "Valid email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_active:
                return Response(
                    {"message": "User is already verified"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            otp = EmailVerificationCode.generate_code()
            EmailVerificationCode.objects.filter(user=user).delete()
            EmailVerificationCode.objects.create(user=user, otp=otp)
            send_mail(
                subject="Your Verification Code",
                message=f"Use this code to verify your account: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(
                {"message": "Verification code resent successfully"},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Failed to send verification code"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code_input = serializer.validated_data['otp']  

            try:
                user = CustomUser.objects.get(email=email)
                code_entry = EmailVerificationCode.objects.filter(user=user).latest('created_at')

                if code_entry.otp == code_input and not code_entry.is_expired():
                    user.is_active = True
                    user.save()
                    return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

                return Response({"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except EmailVerificationCode.DoesNotExist:
                return Response({"error": "No verification code found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user and user.is_active:
                return Response({
                    "message": "Login successful",
                    "user": CustomUserSerializer(user).data
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials or unverified account"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# yourapp/views.py


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        serializer = PasswordResetConfirmSerializer(data={**request.data, 'token': token})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter    






class postview(APIView):
    def post(self , request):
        serializer = postserializer(data=request.data)
        if serializer.is_valid():
            # Save the post
            post = serializer.save()
            # Assign all users as recipients
            all_users = CustomUser.objects.all()
            post.recipients.set(all_users)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserPostsView(APIView):
    def get(self, request):
        user = request.user
        posts = postmodel.objects.filter(recipients=user)
        serializer = postserializer(posts, many=True)
        return Response(serializer.data)