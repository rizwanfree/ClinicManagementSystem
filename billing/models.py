from django.db import models

from appointments.models import Appointment
from patients.models import Patient

# Create your models here.

class Bill(models.Model):
    PAYMENT_STATUS = [
        ("PAID", "Paid"),
        ("PENDING", "Pending"),
        ("CANCELLED", "Cancelled"),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PENDING")
    payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.patient}"