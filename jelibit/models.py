from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
from datetime import date
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name=None, date_of_birth=None,  password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False  # Require email verification
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.TextField()
    date_of_birth=models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = timezone.now() - timedelta(minutes=2)
        CustomUser.objects.filter(is_active=False, created_at__lt=expiration_time).delete()   
        

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999)}"
    
    def send_otp_email(user, otp):
        subject = "Your OTP Code"
        message = f"Hello {user.username},\n\nYour OTP code is {otp}. It will expire in 10 minutes."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    

  




class postmodel(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(CustomUser, related_name='broadcast_posts', blank=True)

    def __str__(self):
        return self.text