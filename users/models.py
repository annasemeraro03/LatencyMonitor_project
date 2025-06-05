from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_researcher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.username