from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_researcher = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username