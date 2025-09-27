from django.db import models

# Create your models here.

class Bill(models.Model):
    PAYMENT_STATUS = [("PAID", "Paid"), ("PENDING", "Pending"), ("CANCELLED", "Cancelled")]

    appointment = models.OneToOneField("appointments.Appointment", on_delete=models.SET_NULL, null=True, blank=True, related_name="bill")
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="bills")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PENDING")
    payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Bill #{self.id} - {self.patient}"