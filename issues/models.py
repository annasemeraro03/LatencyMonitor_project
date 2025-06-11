from django.db import models
from django.conf import settings

class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('approved', 'Approvata'),
        ('rejected', 'Rifiutata'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
