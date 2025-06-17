from django.conf import settings
from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

class LoginRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.timestamp}"

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user and user.is_authenticated:
        LoginRecord.objects.create(user=user)
