from django.utils import timezone
from django.db import models, transaction

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("SCHEDULED", "Scheduled"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey("doctors.Doctor", on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    token_number = models.PositiveIntegerField(null=True, blank=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SCHEDULED")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        constraints = [
            models.UniqueConstraint(fields=["date", "doctor", "token_number"], name="unique_token_per_doctor_day")
        ]

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date} (Token {self.token_number})"

    def _assign_token(self):
        """Assign next token number for (date, doctor) safely."""
        with transaction.atomic():
            # find last token for this (date, doctor)
            last = (
                Appointment.objects
                .select_for_update()
                .filter(date=self.date, doctor=self.doctor)
                .exclude(token_number__isnull=True)
                .order_by("-token_number")
                .first()
            )
            if last and last.token_number:
                candidate = last.token_number + 1
            else:
                candidate = 1
            # ensure uniqueness
            while Appointment.objects.filter(date=self.date, doctor=self.doctor, token_number=candidate).exists():
                candidate += 1
            return candidate

    def save(self, *args, **kwargs):
        if self.token_number is None:
            self.token_number = self._assign_token()
        super().save(*args, **kwargs)