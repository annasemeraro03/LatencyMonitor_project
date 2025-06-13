from django.db import models
import csv
from django.conf import settings

class Device(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Experiment(models.Model):
    MODE_CHOICES = [
        ('photo', 'Photo Mode'),
        ('video', 'Video Mode'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='experiments')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_experiments', null=True, blank=True
    )
    last_modified_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    data_file = models.FileField(upload_to='datasets/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, help_text="Nome del file CSV caricato")

    def __str__(self):
        return f"{self.device} - {self.get_mode_display()} ({self.created_at.date()})"


class PhotodiodeData(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='photodiode_data')
    index = models.PositiveIntegerField()
    value = models.FloatField()
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PhotodiodeData {self.index}"


class LatencyData(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='latency_data')
    index = models.PositiveIntegerField()
    value = models.FloatField()
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"LatencyData {self.index}"
