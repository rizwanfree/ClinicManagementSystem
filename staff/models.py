from django.db import models

# Create your models here.

class Staff(models.Model):
    ROLE_CHOICES = [
        ("RECEPTIONIST", "Receptionist"),
        ("NURSE", "Nurse"),
        ("ADMIN", "Admin"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"