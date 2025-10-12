from datetime import timedelta
import uuid
from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser, postmodel
from rest_framework import serializers
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import PasswordResetToken,CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Or a custom user model
        fields = ['name', 'email', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data['name'],  # Assuming name is used as username
            email=validated_data['email'],
            date_of_birth=['date_of_birth'],
            password=validated_data['password'],
            # Add date_of_birth if using a custom user model
        )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_active', 'is_staff','name','date_of_birth']



class postserializer(serializers.ModelSerializer):
    recipients = CustomUserSerializer(many=True, read_only=True)  
    class Meta:
        model = postmodel 
        fields = '__all__'    




class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        
        # Create or update reset token
        token, created = PasswordResetToken.objects.get_or_create(
            user=user,
            defaults={
                'token': uuid.uuid4(),
                'expires_at': timezone.now() + timedelta(hours=1)
            }
        )
        if not created:
            token.token = uuid.uuid4()
            token.expires_at = timezone.now() + timedelta(hours=1)
            token.save()

        # Send reset email
        reset_link = f"https://liftoff-mmaa.onrender.com/api/password_reset/confirm/{token.token}/"
        send_mail(
            subject='Password Reset Request',
            message=f'Click the link to reset your password: {reset_link}',
            from_email='belloabdulrahmon345@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        return token

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(token=value)
            if reset_token.expires_at < timezone.now():
                raise serializers.ValidationError("This token has expired.")
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        return value

    def save(self):
        token = PasswordResetToken.objects.get(token=self.validated_data['token'])
        user = token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        token.delete()  # Delete token after use
        return user