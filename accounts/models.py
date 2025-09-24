from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("STAFF", "Staff"),        
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="PATIENT")

    def __str__(self):
        return f"{self.username} ({self.role})"