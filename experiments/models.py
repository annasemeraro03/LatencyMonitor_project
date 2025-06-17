import csv, os, logging
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='experiments', null=True, blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_experiments', null=True, blank=True
    )
    last_modified_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    data_file = models.FileField(upload_to='datasets/', blank=True, null=True)
    
    def delete(self, *args, **kwargs):
        """Override per eliminare i file e dati correlati"""
        if self.data_file:
            try:
                print(self.data_file.path)
                if os.path.isfile(self.data_file.path):
                    os.remove(self.data_file.path)
            except Exception as e:
                logging.error(f"Error deleting file for experiment {self.id}: {str(e)}")
        
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.device} - {self.get_mode_display()} - Date: {self.created_at.date()} (ID:{self.id})"

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

@receiver(pre_delete, sender=Experiment)
def delete_experiment_files(sender, instance, **kwargs):
    """Elimina i dati correlati quando un esperimento viene cancellato"""
    instance.photodiode_data.all().delete()
    instance.latency_data.all().delete()
    if instance.data_file:
        try:
            instance.data_file.delete(save=False)
        except Exception as e:
            print(f"Errore eliminando il file: {str(e)}")