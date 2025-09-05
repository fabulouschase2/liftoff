from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import CustomUser, postmodel


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
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
            # Add date_of_birth if using a custom user model
        )
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


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
