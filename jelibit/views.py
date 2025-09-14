from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser, EmailVerificationCode, postmodel
from .serializers import (
    RegisterSerializer, VerifyEmailSerializer,
    LoginSerializer, CustomUserSerializer, postserializer
)


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
                fail_silently=True,
            )

            return Response({"message": "User registered. Verification code sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class resendotp (APIView): 
    def resend_otp(request):
        if request.method == 'GET':
            get_user = request.GET(CustomUser.email)
            if CustomUser.objects.filter(username = get_user).exists() and not CustomUser.objects.get(username = get_user).is_active:
                user = CustomUser.objects.get(username=get_user)
                otp = EmailVerificationCode.generate_code()
                EmailVerificationCode.objects.create(user=user, otp=otp)
                send_mail(
                "Your verification code",
                f"Use this code to verify your account: {otp}",
                "belloabdulrahmon345@gmail.com",
                [user.email],
                fail_silently=True,
            )
                return Response({"message":"Verification Code Resend"},status=status.HTTP_200_OK)
    
        return Response({"message":"Can't Send Verification Code "},status=status.HTTP_404_NOT_FOUND)
    

class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code_input = serializer.validated_data['otp']
            expiration_time = timezone.now() - timedelta(minutes=10)
            CustomUser.objects.filter(is_active=False, created_at__lt=expiration_time).delete()   

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