from django.db import models

from doctors.models import Doctor
from patients.models import Patient

# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    token_number = models.PositiveIntegerField(editable=False, null=True, blank=True)  # new field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Assign token number only if not already set
        if not self.token_number:
            last_appt = (
                Appointment.objects.filter(date=self.date, doctor=self.doctor)
                .exclude(token_number__isnull=True)   # 🚀 ignore null tokens
                .order_by("token_number")
                .last()
            )

            if last_appt and last_appt.token_number:
                self.token_number = last_appt.token_number + 1
            else:
                self.token_number = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date} (Token {self.token_number})"