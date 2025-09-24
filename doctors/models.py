from django.db import models

# Create your models here.
class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True)  # could later become proper schedule

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"