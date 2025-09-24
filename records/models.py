from django.db import models

from patients.models import Patient
from doctors.models import Doctor

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.visit_date}"

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="prescriptions")
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medication_name} ({self.record.patient})"
