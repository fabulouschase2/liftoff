from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

@shared_task
def cleanup_unverified_users():
    cutoff = timezone.now() - timedelta(minutes=5)
    CustomUser.objects.filter(is_verified=False, date_joined__lt=cutoff).delete()
